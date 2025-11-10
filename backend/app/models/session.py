"""
Session Model - SQLAlchemy
Tracks active user sessions for security and "logout all devices" functionality
"""
from sqlalchemy import Column, String, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from ..database import Base


class Session(Base):
    """User session tracking model"""

    __tablename__ = "sessions"

    # Primary Key
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    # Foreign Key
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    # Session Data
    session_token = Column(String(255), unique=True, nullable=False, index=True)  # Hashed
    refresh_token = Column(String(255), unique=True, nullable=True, index=True)  # Hashed

    # Device/Browser Information
    user_agent = Column(String(500), nullable=True)
    ip_address = Column(String(45), nullable=True)  # IPv4 or IPv6
    device_info = Column(Text, nullable=True)  # JSON with device details

    # Session Status
    is_active = Column(Boolean, default=True, nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    last_activity = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="sessions")

    def __repr__(self):
        return f"<Session {self.id} for User {self.user_id}>"


    def is_expired(self) -> bool:
        """Check if session is expired"""
        from datetime import datetime
        return datetime.utcnow() > self.expires_at
