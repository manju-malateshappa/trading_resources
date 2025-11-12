"""
Authentication Endpoints
Handles user registration, login, 2FA, token management
"""
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import json

from ...database import get_db
from ...models.user import User
from ...models.session import Session as UserSession
from ...schemas.auth import (
    UserRegisterRequest, UserRegisterResponse,
    LoginRequest, LoginResponse, Login2FARequired,
    Verify2FARequest, Verify2FAResponse,
    Setup2FAResponse, Enable2FARequest, Disable2FARequest,
    MessageResponse
)
from ...core.security import (
    hash_password, verify_password,
    create_access_token, create_refresh_token,
    generate_totp_secret, generate_totp_uri, generate_qr_code, verify_totp,
    generate_backup_codes, encrypt_secret, decrypt_secret,
    generate_session_token
)
from ...config import settings
from ..dependencies import get_current_user

router = APIRouter()


# ============================================================================
# REGISTRATION
# ============================================================================

@router.post("/register", response_model=UserRegisterResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserRegisterRequest,
    db: Session = Depends(get_db)
):
    """
    Register a new user account

    - **email**: Valid email address
    - **username**: Unique username (3-50 characters, alphanumeric, _, -)
    - **password**: Strong password (min 8 chars, uppercase, lowercase, digit)
    - **full_name**: Optional full name
    """
    # Check if user exists
    existing_user = db.query(User).filter(
        (User.email == user_data.email) | (User.username == user_data.username)
    ).first()

    if existing_user:
        if existing_user.email == user_data.email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )

    # Create new user
    hashed_pw = hash_password(user_data.password)
    new_user = User(
        email=user_data.email,
        username=user_data.username,
        hashed_password=hashed_pw,
        full_name=user_data.full_name
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return UserRegisterResponse(
        user_id=new_user.id,
        email=new_user.email,
        username=new_user.username,
        message="Registration successful. Please log in."
    )


# ============================================================================
# LOGIN
# ============================================================================

@router.post("/login")
async def login(
    credentials: LoginRequest,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    User login

    Returns access & refresh tokens if 2FA is disabled.
    Returns temp token if 2FA is enabled (requires /verify-2fa next).
    """
    # Find user by email or username
    user = db.query(User).filter(
        (User.email == credentials.username_or_email) |
        (User.username == credentials.username_or_email)
    ).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    # Check if account is locked
    if user.locked_until and user.locked_until > datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_423_LOCKED,
            detail=f"Account locked until {user.locked_until.isoformat()}"
        )

    # Verify password
    if not verify_password(credentials.password, user.hashed_password):
        # Increment failed attempts
        user.failed_login_attempts += 1

        # Lock account after 5 failed attempts
        if user.failed_login_attempts >= settings.LOGIN_RATE_LIMIT_PER_15MIN:
            user.locked_until = datetime.utcnow() + timedelta(minutes=15)

        db.commit()

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    # Reset failed attempts on successful password verification
    user.failed_login_attempts = 0
    user.locked_until = None

    # Check if 2FA is enabled
    if user.is_2fa_enabled:
        # Generate temporary token for 2FA verification (5 min expiry)
        temp_token = create_access_token(
            data={"sub": user.id, "purpose": "2fa"},
            expires_delta=timedelta(minutes=5)
        )

        db.commit()

        return Login2FARequired(
            requires_2fa=True,
            temp_token=temp_token,
            message="Please enter your 2FA code"
        )

    # 2FA not enabled - complete login
    user.last_login = datetime.utcnow()
    db.commit()

    # Create tokens
    access_token = create_access_token(data={"sub": user.id})
    refresh_token = create_refresh_token(data={"sub": user.id})

    # Create session
    session_token = generate_session_token()
    new_session = UserSession(
        user_id=user.id,
        session_token=hash_password(session_token),
        refresh_token=hash_password(refresh_token),
        user_agent=request.headers.get("user-agent"),
        ip_address=request.client.host,
        expires_at=datetime.utcnow() + timedelta(hours=settings.SESSION_EXPIRE_HOURS)
    )
    db.add(new_session)
    db.commit()

    return LoginResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        user={
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "full_name": user.full_name
        }
    )


# ============================================================================
# 2FA SETUP
# ============================================================================

@router.get("/2fa/setup", response_model=Setup2FAResponse)
async def setup_2fa(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Setup 2FA for user account

    Returns:
    - TOTP secret
    - QR code (base64 image)
    - Backup codes

    User must call /2fa/enable with first TOTP code to activate.
    """
    if current_user.is_2fa_enabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="2FA already enabled"
        )

    # Generate TOTP secret
    secret = generate_totp_secret()

    # Generate QR code
    uri = generate_totp_uri(secret, current_user.email)
    qr_code = generate_qr_code(uri)

    # Generate backup codes
    backup_codes = generate_backup_codes(settings.BACKUP_CODES_COUNT)

    # Store encrypted secret (not enabled yet)
    encrypted_secret = encrypt_secret(secret)
    current_user.totp_secret = encrypted_secret

    # Store hashed backup codes
    hashed_codes = [hash_password(code) for code in backup_codes]
    current_user.backup_codes = json.dumps(hashed_codes)

    db.commit()

    return Setup2FAResponse(
        secret=secret,
        qr_code=qr_code,
        backup_codes=backup_codes,
        message="Scan QR code with Google Authenticator or Authy. Save backup codes securely."
    )


# ============================================================================
# PLACEHOLDER: AUTHENTICATION DEPENDENCY
# ============================================================================

async def get_current_user(
    # token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """
    Dependency to get current authenticated user from JWT token
    TODO: Implement full JWT validation and user extraction
    """
    # This is a placeholder - full implementation needed
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Authentication dependency not fully implemented yet"
    )


# ============================================================================
# LOGOUT
# ============================================================================

@router.post("/logout", response_model=MessageResponse)
async def logout(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Logout current session
    Invalidates the session token
    """
    # TODO: Implement session invalidation
    return MessageResponse(message="Logged out successfully")
