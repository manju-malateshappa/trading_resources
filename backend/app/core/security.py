"""
Security Utilities: JWT, Password Hashing, 2FA, Encryption
"""
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import secrets
import string
from passlib.context import CryptContext
from jose import JWTError, jwt
import pyotp
import qrcode
import io
import base64
from cryptography.fernet import Fernet
from ..config import settings

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ============================================================================
# PASSWORD UTILITIES
# ============================================================================

def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt

    Note: bcrypt has a 72-byte limit, so we truncate the password if needed
    """
    # Truncate password to 72 bytes (bcrypt limit)
    password_bytes = password.encode('utf-8')[:72]
    password_truncated = password_bytes.decode('utf-8', errors='ignore')
    return pwd_context.hash(password_truncated)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against its hash

    Note: Applies same 72-byte truncation as hash_password
    """
    # Truncate password to 72 bytes (same as hash_password)
    password_bytes = plain_password.encode('utf-8')[:72]
    password_truncated = password_bytes.decode('utf-8', errors='ignore')
    return pwd_context.verify(password_truncated, hashed_password)


# ============================================================================
# JWT TOKEN UTILITIES
# ============================================================================

def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """
    Create JWT access token

    Args:
        data: Data to encode in token (usually {"sub": user_id})
        expires_delta: Optional custom expiration time

    Returns:
        Encoded JWT token
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": "access"
    })

    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def create_refresh_token(data: Dict[str, Any]) -> str:
    """
    Create JWT refresh token (longer expiration)

    Args:
        data: Data to encode in token

    Returns:
        Encoded JWT refresh token
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": "refresh"
    })

    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Decode and validate JWT token

    Args:
        token: JWT token to decode

    Returns:
        Token payload if valid, None otherwise
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None


def extract_user_id_from_token(token: str) -> Optional[str]:
    """Extract user ID from token"""
    payload = decode_token(token)
    if payload:
        return payload.get("sub")
    return None


# ============================================================================
# 2FA / TOTP UTILITIES
# ============================================================================

def generate_totp_secret() -> str:
    """
    Generate a random TOTP secret for 2FA

    Returns:
        Base32 encoded secret (32 characters)
    """
    return pyotp.random_base32()


def generate_totp_uri(secret: str, username: str) -> str:
    """
    Generate TOTP provisioning URI for QR code

    Args:
        secret: TOTP secret
        username: User's username/email

    Returns:
        TOTP URI string
    """
    return pyotp.totp.TOTP(secret).provisioning_uri(
        name=username,
        issuer_name=settings.TOTP_ISSUER
    )


def generate_qr_code(uri: str) -> str:
    """
    Generate QR code image from TOTP URI

    Args:
        uri: TOTP provisioning URI

    Returns:
        Base64 encoded PNG image
    """
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(uri)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    # Convert to base64
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    img_str = base64.b64encode(buffer.getvalue()).decode()

    return f"data:image/png;base64,{img_str}"


def verify_totp(secret: str, token: str) -> bool:
    """
    Verify TOTP token

    Args:
        secret: User's TOTP secret
        token: 6-digit code from authenticator app

    Returns:
        True if valid, False otherwise
    """
    totp = pyotp.TOTP(secret)
    return totp.verify(token, valid_window=1)  # Allow 1 step before/after


def generate_backup_codes(count: int = 10) -> list[str]:
    """
    Generate backup codes for 2FA recovery

    Args:
        count: Number of codes to generate

    Returns:
        List of backup codes
    """
    codes = []
    for _ in range(count):
        # Generate 8-character alphanumeric code
        code = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(8))
        # Format as XXXX-XXXX for readability
        formatted = f"{code[:4]}-{code[4:]}"
        codes.append(formatted)
    return codes


# ============================================================================
# ENCRYPTION UTILITIES (for storing TOTP secrets)
# ============================================================================

def get_encryption_key() -> bytes:
    """
    Get or generate encryption key for sensitive data
    In production, this should be stored securely (e.g., environment variable or secret manager)
    """
    # Use SECRET_KEY as base, but derive a proper Fernet key
    key = base64.urlsafe_b64encode(settings.SECRET_KEY.encode()[:32].ljust(32, b'0'))
    return key


def encrypt_secret(plaintext: str) -> str:
    """
    Encrypt sensitive data (e.g., TOTP secret)

    Args:
        plaintext: String to encrypt

    Returns:
        Encrypted string
    """
    fernet = Fernet(get_encryption_key())
    encrypted = fernet.encrypt(plaintext.encode())
    return base64.urlsafe_b64encode(encrypted).decode()


def decrypt_secret(encrypted: str) -> str:
    """
    Decrypt sensitive data

    Args:
        encrypted: Encrypted string

    Returns:
        Decrypted plaintext
    """
    fernet = Fernet(get_encryption_key())
    decoded = base64.urlsafe_b64decode(encrypted.encode())
    decrypted = fernet.decrypt(decoded)
    return decrypted.decode()


# ============================================================================
# SESSION UTILITIES
# ============================================================================

def generate_session_token() -> str:
    """Generate a secure random session token"""
    return secrets.token_urlsafe(32)


def hash_session_token(token: str) -> str:
    """Hash a session token for storage"""
    return hash_password(token)


def verify_session_token(token: str, hashed_token: str) -> bool:
    """Verify a session token against its hash"""
    return verify_password(token, hashed_token)
