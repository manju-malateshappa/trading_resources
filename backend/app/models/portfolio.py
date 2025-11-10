"""
Portfolio Model - SQLAlchemy
Stores user portfolio and position data
"""
from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Integer, Text, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum
from ..database import Base


class PortfolioType(str, enum.Enum):
    """Portfolio account types"""
    TFSA = "tfsa"
    RRSP = "rrsp"
    TAXABLE = "taxable"
    PAPER = "paper"  # Paper trading


class Portfolio(Base):
    """User portfolio model"""

    __tablename__ = "portfolios"

    # Primary Key
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    # Foreign Key
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    # Portfolio Info
    name = Column(String(100), nullable=False)
    portfolio_type = Column(Enum(PortfolioType), default=PortfolioType.PAPER, nullable=False)
    description = Column(Text, nullable=True)

    # Financial Data
    initial_cash = Column(Float, default=10000.0, nullable=False)
    current_cash = Column(Float, default=10000.0, nullable=False)
    total_value = Column(Float, default=10000.0, nullable=False)  # Cash + positions
    total_return = Column(Float, default=0.0, nullable=False)  # Percentage
    total_gain_loss = Column(Float, default=0.0, nullable=False)  # Dollar amount

    # Settings
    is_active = Column(Boolean, default=True, nullable=False)
    is_default = Column(Boolean, default=False, nullable=False)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    user = relationship("User", back_populates="portfolios")
    positions = relationship("Position", back_populates="portfolio", cascade="all, delete-orphan")
    trades = relationship("Trade", back_populates="portfolio", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Portfolio {self.name} (${self.total_value:.2f})>"


class Position(Base):
    """Current stock positions in portfolio"""

    __tablename__ = "positions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    portfolio_id = Column(String(36), ForeignKey("portfolios.id", ondelete="CASCADE"), nullable=False)

    # Stock Info
    symbol = Column(String(20), nullable=False, index=True)
    name = Column(String(100), nullable=True)

    # Position Data
    shares = Column(Float, nullable=False)
    avg_cost = Column(Float, nullable=False)  # Average cost per share
    current_price = Column(Float, nullable=False)
    market_value = Column(Float, nullable=False)  # shares * current_price

    # P&L
    unrealized_gain_loss = Column(Float, nullable=False)
    unrealized_gain_loss_pct = Column(Float, nullable=False)

    # Timestamps
    opened_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    portfolio = relationship("Portfolio", back_populates="positions")

    def __repr__(self):
        return f"<Position {self.symbol} x{self.shares}>"


class Trade(Base):
    """Trade history"""

    __tablename__ = "trades"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    portfolio_id = Column(String(36), ForeignKey("portfolios.id", ondelete="CASCADE"), nullable=False)

    # Trade Info
    symbol = Column(String(20), nullable=False, index=True)
    action = Column(String(10), nullable=False)  # BUY, SELL
    shares = Column(Float, nullable=False)
    price = Column(Float, nullable=False)
    total_value = Column(Float, nullable=False)  # shares * price
    fees = Column(Float, default=0.0, nullable=False)

    # Analysis
    reason = Column(Text, nullable=True)  # Why this trade was made
    investment_score = Column(Float, nullable=True)  # Score at time of trade

    # Timestamps
    executed_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    portfolio = relationship("Portfolio", back_populates="trades")

    def __repr__(self):
        return f"<Trade {self.action} {self.symbol} x{self.shares} @ ${self.price}>"
