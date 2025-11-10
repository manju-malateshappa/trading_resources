"""
Authentication Pydantic Schemas
Request/Response models for authentication endpoints
"""
from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from datetime import datetime


# ============================================================================
# REGISTRATION
# ============================================================================

class UserRegisterRequest(BaseModel):
    """User registration request"""
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50, pattern="^[a-zA-Z0-9_-]+$")
    password: str = Field(..., min_length=8, max_length=100)
    full_name: Optional[str] = Field(None, max_length=100)

    @validator('password')
    def validate_password(cls, v):
        """Validate password strength"""
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        return v


class UserRegisterResponse(BaseModel):
    """User registration response"""
    user_id: str
    email: str
    username: str
    message: str = "Registration successful"


# ============================================================================
# LOGIN
# ============================================================================

class LoginRequest(BaseModel):
    """User login request"""
    username_or_email: str
    password: str


class LoginResponse(BaseModel):
    """User login response (without 2FA)"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: dict


class Login2FARequired(BaseModel):
    """Response when 2FA is required"""
    requires_2fa: bool = True
    temp_token: str  # Temporary token for 2FA verification
    message: str = "2FA verification required"


# ============================================================================
# 2FA VERIFICATION
# ============================================================================

class Verify2FARequest(BaseModel):
    """2FA verification request"""
    temp_token: str
    totp_code: str = Field(..., min_length=6, max_length=6, pattern="^[0-9]+$")


class Verify2FAResponse(BaseModel):
    """2FA verification response"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: dict


# ============================================================================
# 2FA SETUP
# ============================================================================

class Setup2FAResponse(BaseModel):
    """2FA setup response"""
    secret: str
    qr_code: str  # Base64 encoded QR code image
    backup_codes: list[str]
    message: str = "Scan QR code with authenticator app"


class Enable2FARequest(BaseModel):
    """Enable 2FA request (confirm with first TOTP code)"""
    totp_code: str = Field(..., min_length=6, max_length=6, pattern="^[0-9]+$")


class Disable2FARequest(BaseModel):
    """Disable 2FA request"""
    password: str
    totp_code: str = Field(..., min_length=6, max_length=6, pattern="^[0-9]+$")


# ============================================================================
# TOKEN MANAGEMENT
# ============================================================================

class TokenRefreshRequest(BaseModel):
    """Token refresh request"""
    refresh_token: str


class TokenRefreshResponse(BaseModel):
    """Token refresh response"""
    access_token: str
    token_type: str = "bearer"


# ============================================================================
# PASSWORD MANAGEMENT
# ============================================================================

class PasswordChangeRequest(BaseModel):
    """Password change request"""
    current_password: str
    new_password: str = Field(..., min_length=8, max_length=100)

    @validator('new_password')
    def validate_new_password(cls, v):
        """Validate password strength"""
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        return v


class PasswordResetRequest(BaseModel):
    """Password reset request (via email)"""
    email: EmailStr


class PasswordResetConfirm(BaseModel):
    """Password reset confirmation"""
    token: str
    new_password: str = Field(..., min_length=8, max_length=100)


# ============================================================================
# SESSION MANAGEMENT
# ============================================================================

class SessionInfo(BaseModel):
    """Session information"""
    session_id: str
    device_info: Optional[str]
    ip_address: Optional[str]
    created_at: datetime
    last_activity: datetime
    is_current: bool = False

    class Config:
        from_attributes = True


class ActiveSessionsResponse(BaseModel):
    """List of active sessions"""
    sessions: list[SessionInfo]
    total: int


# ============================================================================
# GENERAL RESPONSES
# ============================================================================

class MessageResponse(BaseModel):
    """Generic message response"""
    message: str
    success: bool = True
