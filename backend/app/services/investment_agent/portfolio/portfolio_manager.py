"""Portfolio management module for tracking and managing investments."""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import sqlite3
from pathlib import Path

from ..utils.logger import logger
from ..utils.config_loader import config


class Portfolio:
    """Represents an investment portfolio."""

    def __init__(self, name: str = "Main Portfolio", initial_capital: float = 100000):
        """Initialize portfolio.

        Args:
            name: Portfolio name
            initial_capital: Starting capital
        """
        self.name = name
        self.initial_capital = initial_capital
        self.cash = initial_capital
        self.positions: Dict[str, Position] = {}
        self.trades: List[Trade] = []
        self.created_at = datetime.now()

    def add_position(
        self,
        symbol: str,
        shares: float,
        entry_price: float,
        entry_date: datetime = None
    ) -> None:
        """Add or update a position.

        Args:
            symbol: Stock symbol
            shares: Number of shares
            entry_price: Entry price per share
            entry_date: Entry date (default: now)
        """
        if entry_date is None:
            entry_date = datetime.now()

        cost = shares * entry_price

        if symbol in self.positions:
            # Update existing position
            position = self.positions[symbol]
            total_shares = position.shares + shares
            total_cost = position.cost_basis + cost
            position.shares = total_shares
            position.cost_basis = total_cost
            position.average_price = total_cost / total_shares if total_shares > 0 else 0
        else:
            # Create new position
            self.positions[symbol] = Position(
                symbol=symbol,
                shares=shares,
                entry_price=entry_price,
                entry_date=entry_date
            )

        self.cash -= cost

        # Record trade
        self.trades.append(Trade(
            symbol=symbol,
            action='BUY',
            shares=shares,
            price=entry_price,
            date=entry_date,
            total=cost
        ))

        logger.info(f"Added {shares} shares of {symbol} at ${entry_price:.2f}")

    def remove_position(
        self,
        symbol: str,
        shares: float,
        exit_price: float,
        exit_date: datetime = None
    ) -> Optional[float]:
        """Remove or reduce a position.

        Args:
            symbol: Stock symbol
            shares: Number of shares to sell
            exit_price: Exit price per share
            exit_date: Exit date (default: now)

        Returns:
            Profit/loss from the sale
        """
        if exit_date is None:
            exit_date = datetime.now()

        if symbol not in self.positions:
            logger.warning(f"No position found for {symbol}")
            return None

        position = self.positions[symbol]

        if shares > position.shares:
            logger.warning(f"Cannot sell {shares} shares of {symbol}, only have {position.shares}")
            shares = position.shares

        proceeds = shares * exit_price
        cost_basis = (position.cost_basis / position.shares) * shares if position.shares > 0 else 0
        profit = proceeds - cost_basis

        # Update position
        position.shares -= shares
        position.cost_basis -= cost_basis

        if position.shares <= 0:
            del self.positions[symbol]

        self.cash += proceeds

        # Record trade
        self.trades.append(Trade(
            symbol=symbol,
            action='SELL',
            shares=shares,
            price=exit_price,
            date=exit_date,
            total=proceeds,
            profit=profit
        ))

        logger.info(f"Sold {shares} shares of {symbol} at ${exit_price:.2f}, P/L: ${profit:.2f}")

        return profit

    def get_position_value(self, symbol: str, current_price: float) -> float:
        """Get current value of a position.

        Args:
            symbol: Stock symbol
            current_price: Current price

        Returns:
            Current market value
        """
        if symbol not in self.positions:
            return 0.0

        return self.positions[symbol].shares * current_price

    def get_total_value(self, current_prices: Dict[str, float]) -> float:
        """Get total portfolio value.

        Args:
            current_prices: Dictionary of current prices

        Returns:
            Total portfolio value
        """
        positions_value = sum(
            pos.shares * current_prices.get(symbol, 0)
            for symbol, pos in self.positions.items()
        )

        return self.cash + positions_value

    def get_return(self, current_prices: Dict[str, float]) -> float:
        """Get total return.

        Args:
            current_prices: Dictionary of current prices

        Returns:
            Total return percentage
        """
        current_value = self.get_total_value(current_prices)
        return (current_value - self.initial_capital) / self.initial_capital

    def get_allocation(self, current_prices: Dict[str, float]) -> Dict[str, float]:
        """Get portfolio allocation.

        Args:
            current_prices: Dictionary of current prices

        Returns:
            Dictionary of symbol: allocation percentage
        """
        total_value = self.get_total_value(current_prices)

        if total_value == 0:
            return {}

        allocation = {}

        for symbol, position in self.positions.items():
            value = position.shares * current_prices.get(symbol, 0)
            allocation[symbol] = value / total_value

        allocation['CASH'] = self.cash / total_value

        return allocation

    def to_dict(self) -> Dict:
        """Convert portfolio to dictionary.

        Returns:
            Portfolio data as dictionary
        """
        return {
            'name': self.name,
            'initial_capital': self.initial_capital,
            'cash': self.cash,
            'positions': {
                symbol: pos.to_dict()
                for symbol, pos in self.positions.items()
            },
            'trades': [trade.to_dict() for trade in self.trades],
            'created_at': self.created_at.isoformat(),
        }


class Position:
    """Represents a stock position."""

    def __init__(
        self,
        symbol: str,
        shares: float,
        entry_price: float,
        entry_date: datetime
    ):
        """Initialize position."""
        self.symbol = symbol
        self.shares = shares
        self.entry_price = entry_price
        self.average_price = entry_price
        self.cost_basis = shares * entry_price
        self.entry_date = entry_date

    def get_return(self, current_price: float) -> float:
        """Get position return.

        Args:
            current_price: Current stock price

        Returns:
            Return percentage
        """
        if self.average_price == 0:
            return 0.0

        return (current_price - self.average_price) / self.average_price

    def get_profit_loss(self, current_price: float) -> float:
        """Get unrealized profit/loss.

        Args:
            current_price: Current stock price

        Returns:
            Profit/loss in dollars
        """
        current_value = self.shares * current_price
        return current_value - self.cost_basis

    def to_dict(self) -> Dict:
        """Convert position to dictionary."""
        return {
            'symbol': self.symbol,
            'shares': self.shares,
            'entry_price': self.entry_price,
            'average_price': self.average_price,
            'cost_basis': self.cost_basis,
            'entry_date': self.entry_date.isoformat(),
        }


class Trade:
    """Represents a trade."""

    def __init__(
        self,
        symbol: str,
        action: str,
        shares: float,
        price: float,
        date: datetime,
        total: float,
        profit: float = 0.0
    ):
        """Initialize trade."""
        self.symbol = symbol
        self.action = action  # BUY or SELL
        self.shares = shares
        self.price = price
        self.date = date
        self.total = total
        self.profit = profit

    def to_dict(self) -> Dict:
        """Convert trade to dictionary."""
        return {
            'symbol': self.symbol,
            'action': self.action,
            'shares': self.shares,
            'price': self.price,
            'date': self.date.isoformat(),
            'total': self.total,
            'profit': self.profit,
        }


class PortfolioManager:
    """Manage investment portfolios."""

    def __init__(self, db_path: str = None):
        """Initialize portfolio manager.

        Args:
            db_path: Path to SQLite database
        """
        if db_path is None:
            db_dir = Path(__file__).parent.parent / "data"
            db_dir.mkdir(exist_ok=True)
            db_path = str(db_dir / "portfolio.db")

        self.db_path = db_path
        self.portfolios: Dict[str, Portfolio] = {}
        self._init_database()

    def _init_database(self) -> None:
        """Initialize database tables."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS portfolios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                initial_capital REAL NOT NULL,
                created_at TEXT NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS positions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                portfolio_name TEXT NOT NULL,
                symbol TEXT NOT NULL,
                shares REAL NOT NULL,
                average_price REAL NOT NULL,
                cost_basis REAL NOT NULL,
                entry_date TEXT NOT NULL,
                FOREIGN KEY (portfolio_name) REFERENCES portfolios(name)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS trades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                portfolio_name TEXT NOT NULL,
                symbol TEXT NOT NULL,
                action TEXT NOT NULL,
                shares REAL NOT NULL,
                price REAL NOT NULL,
                total REAL NOT NULL,
                profit REAL DEFAULT 0,
                date TEXT NOT NULL,
                FOREIGN KEY (portfolio_name) REFERENCES portfolios(name)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS portfolio_snapshots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                portfolio_name TEXT NOT NULL,
                date TEXT NOT NULL,
                total_value REAL NOT NULL,
                cash REAL NOT NULL,
                positions_value REAL NOT NULL,
                return_pct REAL NOT NULL,
                FOREIGN KEY (portfolio_name) REFERENCES portfolios(name)
            )
        """)

        conn.commit()
        conn.close()

    def create_portfolio(
        self,
        name: str,
        initial_capital: float = 100000
    ) -> Portfolio:
        """Create a new portfolio.

        Args:
            name: Portfolio name
            initial_capital: Initial capital

        Returns:
            New Portfolio instance
        """
        portfolio = Portfolio(name, initial_capital)
        self.portfolios[name] = portfolio

        # Save to database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            "INSERT OR REPLACE INTO portfolios (name, initial_capital, created_at) VALUES (?, ?, ?)",
            (name, initial_capital, portfolio.created_at.isoformat())
        )

        conn.commit()
        conn.close()

        logger.info(f"Created portfolio '{name}' with ${initial_capital:,.2f}")

        return portfolio

    def get_portfolio(self, name: str) -> Optional[Portfolio]:
        """Get portfolio by name.

        Args:
            name: Portfolio name

        Returns:
            Portfolio instance or None
        """
        if name in self.portfolios:
            return self.portfolios[name]

        # Try to load from database
        return self.load_portfolio(name)

    def load_portfolio(self, name: str) -> Optional[Portfolio]:
        """Load portfolio from database.

        Args:
            name: Portfolio name

        Returns:
            Portfolio instance or None
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Load portfolio info
        cursor.execute(
            "SELECT initial_capital, created_at FROM portfolios WHERE name = ?",
            (name,)
        )
        row = cursor.fetchone()

        if not row:
            conn.close()
            return None

        initial_capital, created_at = row
        portfolio = Portfolio(name, initial_capital)
        portfolio.created_at = datetime.fromisoformat(created_at)

        # Load positions
        cursor.execute(
            "SELECT symbol, shares, average_price, cost_basis, entry_date FROM positions WHERE portfolio_name = ?",
            (name,)
        )

        total_positions_value = 0
        for row in cursor.fetchall():
            symbol, shares, avg_price, cost_basis, entry_date = row
            position = Position(
                symbol=symbol,
                shares=shares,
                entry_price=avg_price,
                entry_date=datetime.fromisoformat(entry_date)
            )
            position.average_price = avg_price
            position.cost_basis = cost_basis
            portfolio.positions[symbol] = position
            total_positions_value += cost_basis

        # Calculate remaining cash
        portfolio.cash = initial_capital - total_positions_value

        # Load trades
        cursor.execute(
            "SELECT symbol, action, shares, price, total, profit, date FROM trades WHERE portfolio_name = ?",
            (name,)
        )

        for row in cursor.fetchall():
            symbol, action, shares, price, total, profit, date = row
            trade = Trade(
                symbol=symbol,
                action=action,
                shares=shares,
                price=price,
                date=datetime.fromisoformat(date),
                total=total,
                profit=profit
            )
            portfolio.trades.append(trade)

        conn.close()

        self.portfolios[name] = portfolio
        logger.info(f"Loaded portfolio '{name}'")

        return portfolio

    def save_portfolio(self, portfolio: Portfolio) -> None:
        """Save portfolio to database.

        Args:
            portfolio: Portfolio to save
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Update portfolio info
        cursor.execute(
            "INSERT OR REPLACE INTO portfolios (name, initial_capital, created_at) VALUES (?, ?, ?)",
            (portfolio.name, portfolio.initial_capital, portfolio.created_at.isoformat())
        )

        # Delete existing positions and re-insert
        cursor.execute("DELETE FROM positions WHERE portfolio_name = ?", (portfolio.name,))

        for symbol, position in portfolio.positions.items():
            cursor.execute(
                """INSERT INTO positions
                   (portfolio_name, symbol, shares, average_price, cost_basis, entry_date)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (portfolio.name, symbol, position.shares, position.average_price,
                 position.cost_basis, position.entry_date.isoformat())
            )

        # Save new trades (only trades not already in database)
        cursor.execute(
            "SELECT COUNT(*) FROM trades WHERE portfolio_name = ?",
            (portfolio.name,)
        )
        existing_trades = cursor.fetchone()[0]

        for trade in portfolio.trades[existing_trades:]:
            cursor.execute(
                """INSERT INTO trades
                   (portfolio_name, symbol, action, shares, price, total, profit, date)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (portfolio.name, trade.symbol, trade.action, trade.shares,
                 trade.price, trade.total, trade.profit, trade.date.isoformat())
            )

        conn.commit()
        conn.close()

        logger.info(f"Saved portfolio '{portfolio.name}'")

    def save_snapshot(
        self,
        portfolio: Portfolio,
        current_prices: Dict[str, float]
    ) -> None:
        """Save portfolio snapshot for performance tracking.

        Args:
            portfolio: Portfolio instance
            current_prices: Current stock prices
        """
        total_value = portfolio.get_total_value(current_prices)
        positions_value = total_value - portfolio.cash
        return_pct = portfolio.get_return(current_prices)

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """INSERT INTO portfolio_snapshots
               (portfolio_name, date, total_value, cash, positions_value, return_pct)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (portfolio.name, datetime.now().isoformat(), total_value,
             portfolio.cash, positions_value, return_pct)
        )

        conn.commit()
        conn.close()

    def get_performance_history(self, portfolio_name: str) -> pd.DataFrame:
        """Get historical performance data.

        Args:
            portfolio_name: Portfolio name

        Returns:
            DataFrame with historical performance
        """
        conn = sqlite3.connect(self.db_path)

        df = pd.read_sql_query(
            """SELECT date, total_value, cash, positions_value, return_pct
               FROM portfolio_snapshots
               WHERE portfolio_name = ?
               ORDER BY date""",
            conn,
            params=(portfolio_name,)
        )

        conn.close()

        if not df.empty:
            df['date'] = pd.to_datetime(df['date'])
            df.set_index('date', inplace=True)

        return df


__all__ = ['Portfolio', 'Position', 'Trade', 'PortfolioManager']
