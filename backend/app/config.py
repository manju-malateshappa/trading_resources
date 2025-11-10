"""
Application Configuration
Manages all environment variables and settings
"""
from pydantic_settings import BaseSettings
from pydantic import field_validator
from functools import lru_cache
from typing import Optional, Union


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # Application
    APP_NAME: str = "Investment Agent API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    ENVIRONMENT: str = "development"  # development, staging, production

    # API
    API_V1_PREFIX: str = "/api/v1"
    BACKEND_CORS_ORIGINS: Union[list[str], str] = ["http://localhost:3000", "http://localhost:5173"]

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, v):
        """Parse CORS origins from string or list"""
        if isinstance(v, str):
            # Handle comma-separated string
            return [origin.strip() for origin in v.split(",")]
        return v

    # Security
    SECRET_KEY: str = "CHANGE-ME-IN-PRODUCTION-USE-OPENSSL-RAND-HEX-32"  # Required - used for JWT signing
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Password Security
    BCRYPT_ROUNDS: int = 12

    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    LOGIN_RATE_LIMIT_PER_15MIN: int = 5

    # Database (defaults to SQLite for quick testing)
    DATABASE_URL: str = "sqlite:///./investment_agent.db"  # Override with PostgreSQL in production
    DATABASE_POOL_SIZE: int = 5
    DATABASE_MAX_OVERFLOW: int = 10

    # Redis Cache
    REDIS_URL: Optional[str] = None
    REDIS_CACHE_TTL: int = 3600  # 1 hour

    # 2FA
    TOTP_ISSUER: str = "Investment Agent"
    BACKUP_CODES_COUNT: int = 10

    # Session Management
    SESSION_EXPIRE_HOURS: int = 24
    MAX_SESSIONS_PER_USER: int = 5

    # External APIs (from existing .env)
    ALPHA_VANTAGE_API_KEY: Optional[str] = None
    FINNHUB_API_KEY: Optional[str] = None
    FRED_API_KEY: Optional[str] = None
    NEWS_API_KEY: Optional[str] = None

    # Email (for future notifications)
    SMTP_HOST: Optional[str] = None
    SMTP_PORT: int = 587
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAIL_FROM: Optional[str] = None

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: Optional[str] = "logs/app.log"

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()


# Export settings instance
settings = get_settings()
