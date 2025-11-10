"""Risk management module for portfolio management."""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta

from ..portfolio.portfolio_manager import Portfolio
from ..utils.logger import logger
from ..utils.config_loader import config


class RiskManager:
    """Manage portfolio risk and position sizing."""

    def __init__(self):
        """Initialize risk manager."""
        self.config = config
        self.risk_params = config.get_risk_params()

    def calculate_position_size(
        self,
        portfolio: Portfolio,
        symbol: str,
        current_price: float,
        volatility: float = None,
        conviction: float = 1.0
    ) -> Tuple[int, float]:
        """Calculate appropriate position size.

        Args:
            portfolio: Portfolio instance
            symbol: Stock symbol
            current_price: Current stock price
            volatility: Stock volatility (optional)
            conviction: Conviction level 0-1 (default: 1.0)

        Returns:
            Tuple of (shares, position_value)
        """
        # Get portfolio value
        total_value = portfolio.cash  # Simplified - in practice would include positions

        # Maximum position size
        max_position_pct = self.config.get('portfolio.max_position_size', 0.15)
        max_position_value = total_value * max_position_pct

        # Adjust for conviction
        position_value = max_position_value * conviction

        # Calculate shares
        shares = int(position_value / current_price)

        # Ensure we don't exceed cash available
        if shares * current_price > portfolio.cash:
            shares = int(portfolio.cash / current_price)
            position_value = shares * current_price

        logger.info(f"Position size for {symbol}: {shares} shares @ ${current_price:.2f} = ${position_value:,.2f}")

        return shares, position_value

    def check_position_limits(
        self,
        portfolio: Portfolio,
        symbol: str,
        additional_shares: int,
        current_price: float,
        current_prices: Dict[str, float]
    ) -> bool:
        """Check if adding shares would violate position limits.

        Args:
            portfolio: Portfolio instance
            symbol: Stock symbol
            additional_shares: Shares to add
            current_price: Current stock price
            current_prices: Dictionary of all current prices

        Returns:
            True if within limits, False otherwise
        """
        # Calculate new position size
        current_shares = portfolio.positions.get(symbol).shares if symbol in portfolio.positions else 0
        new_shares = current_shares + additional_shares
        new_position_value = new_shares * current_price

        # Get total portfolio value
        total_value = portfolio.get_total_value(current_prices)

        # Check position size limit
        max_position_pct = self.config.get('portfolio.max_position_size', 0.15)
        position_pct = new_position_value / total_value if total_value > 0 else 0

        if position_pct > max_position_pct:
            logger.warning(
                f"Position size {position_pct:.1%} exceeds limit {max_position_pct:.1%}"
            )
            return False

        # Check if we have enough cash
        cost = additional_shares * current_price
        if cost > portfolio.cash:
            logger.warning(f"Insufficient cash: need ${cost:,.2f}, have ${portfolio.cash:,.2f}")
            return False

        return True

    def check_sector_concentration(
        self,
        portfolio: Portfolio,
        symbol: str,
        sector: str,
        additional_value: float,
        current_prices: Dict[str, float],
        sectors: Dict[str, str]
    ) -> bool:
        """Check sector concentration limits.

        Args:
            portfolio: Portfolio instance
            symbol: Stock symbol
            sector: Stock sector
            additional_value: Additional value to add
            current_prices: Dictionary of current prices
            sectors: Dictionary mapping symbols to sectors

        Returns:
            True if within limits, False otherwise
        """
        # Calculate current sector allocation
        total_value = portfolio.get_total_value(current_prices)
        sector_value = 0

        for sym, position in portfolio.positions.items():
            if sectors.get(sym) == sector:
                sector_value += position.shares * current_prices.get(sym, 0)

        # Add new position
        new_sector_value = sector_value + additional_value

        # Check limit
        max_sector_pct = self.config.get('portfolio.max_sector_allocation', 0.30)
        sector_pct = new_sector_value / total_value if total_value > 0 else 0

        if sector_pct > max_sector_pct:
            logger.warning(
                f"Sector {sector} allocation {sector_pct:.1%} exceeds limit {max_sector_pct:.1%}"
            )
            return False

        return True

    def calculate_stop_loss(
        self,
        entry_price: float,
        stop_loss_pct: float = None
    ) -> float:
        """Calculate stop-loss price.

        Args:
            entry_price: Entry price
            stop_loss_pct: Stop-loss percentage (default from config)

        Returns:
            Stop-loss price
        """
        if stop_loss_pct is None:
            stop_loss_pct = self.config.get('strategy.exit.stop_loss', 0.15)

        stop_price = entry_price * (1 - stop_loss_pct)

        logger.debug(f"Stop-loss: ${stop_price:.2f} ({stop_loss_pct:.1%} below ${entry_price:.2f})")

        return stop_price

    def calculate_trailing_stop(
        self,
        entry_price: float,
        current_price: float,
        trailing_stop_pct: float = None
    ) -> Optional[float]:
        """Calculate trailing stop-loss price.

        Args:
            entry_price: Entry price
            current_price: Current price
            trailing_stop_pct: Trailing stop percentage (default from config)

        Returns:
            Trailing stop price or None if not applicable
        """
        if trailing_stop_pct is None:
            trailing_stop_pct = self.config.get('strategy.exit.trailing_stop', 0.10)

        # Only activate trailing stop after 20% gain
        min_gain_for_trailing = 0.20
        gain = (current_price - entry_price) / entry_price

        if gain < min_gain_for_trailing:
            return None

        trailing_stop = current_price * (1 - trailing_stop_pct)

        return trailing_stop

    def calculate_take_profit_levels(
        self,
        entry_price: float
    ) -> Dict[str, float]:
        """Calculate take-profit levels.

        Args:
            entry_price: Entry price

        Returns:
            Dictionary of take-profit levels and percentages to sell
        """
        levels = self.config.get('strategy.exit.take_profit_levels', [0.25, 0.50, 1.00, 2.00])

        take_profits = {}

        for i, level in enumerate(levels):
            target_price = entry_price * (1 + level)
            sell_pct = 0.20  # Default 20% at each level

            # Customize sell percentages
            if i == 0:  # First level (25% gain)
                sell_pct = 0.20
            elif i == 1:  # Second level (50% gain)
                sell_pct = 0.25
            elif i == 2:  # Third level (100% gain)
                sell_pct = 0.30
            else:  # Final level (200% gain)
                sell_pct = 1.0  # Sell everything remaining

            take_profits[f"{level:.0%}"] = {
                'price': target_price,
                'sell_percentage': sell_pct
            }

        return take_profits

    def assess_portfolio_risk(
        self,
        portfolio: Portfolio,
        current_prices: Dict[str, float],
        historical_data: Dict[str, pd.DataFrame]
    ) -> Dict:
        """Assess overall portfolio risk.

        Args:
            portfolio: Portfolio instance
            current_prices: Dictionary of current prices
            historical_data: Historical price data for each position

        Returns:
            Dictionary with risk metrics
        """
        # Calculate portfolio value and return
        total_value = portfolio.get_total_value(current_prices)
        total_return = portfolio.get_return(current_prices)

        # Calculate portfolio volatility
        returns_data = []
        weights = []

        for symbol, position in portfolio.positions.items():
            if symbol in historical_data:
                df = historical_data[symbol]
                if not df.empty and 'Close' in df.columns:
                    returns = df['Close'].pct_change().dropna()
                    returns_data.append(returns)

                    # Weight by position size
                    weight = (position.shares * current_prices.get(symbol, 0)) / total_value
                    weights.append(weight)

        portfolio_volatility = 0
        if returns_data:
            # Combine returns
            combined_returns = pd.concat(returns_data, axis=1)
            combined_returns = combined_returns.fillna(0)

            # Calculate weighted portfolio volatility
            if len(weights) > 0:
                weighted_returns = combined_returns @ weights
                portfolio_volatility = weighted_returns.std() * np.sqrt(252)  # Annualized

        # Calculate maximum drawdown
        max_drawdown = self._calculate_max_drawdown(portfolio, historical_data, current_prices)

        # Calculate concentration
        allocation = portfolio.get_allocation(current_prices)
        max_concentration = max(allocation.values()) if allocation else 0

        # Number of positions
        num_positions = len(portfolio.positions)

        # Risk assessment
        risk_level = self._assess_risk_level(
            portfolio_volatility,
            max_drawdown,
            max_concentration,
            num_positions
        )

        return {
            'total_value': total_value,
            'total_return': total_return,
            'portfolio_volatility': portfolio_volatility,
            'max_drawdown': max_drawdown,
            'max_concentration': max_concentration,
            'num_positions': num_positions,
            'risk_level': risk_level,
            'allocation': allocation,
        }

    def _calculate_max_drawdown(
        self,
        portfolio: Portfolio,
        historical_data: Dict[str, pd.DataFrame],
        current_prices: Dict[str, float]
    ) -> float:
        """Calculate maximum drawdown.

        Args:
            portfolio: Portfolio instance
            historical_data: Historical price data
            current_prices: Current prices

        Returns:
            Maximum drawdown percentage
        """
        # This is a simplified version
        # In practice, you'd calculate the drawdown from historical portfolio values

        max_dd = 0

        for symbol, position in portfolio.positions.items():
            if symbol in historical_data:
                df = historical_data[symbol]
                if not df.empty and 'Close' in df.columns:
                    # Calculate drawdown for this position
                    cummax = df['Close'].expanding().max()
                    drawdown = (df['Close'] - cummax) / cummax

                    position_max_dd = drawdown.min()
                    max_dd = min(max_dd, position_max_dd)

        return abs(max_dd)

    def _assess_risk_level(
        self,
        volatility: float,
        max_drawdown: float,
        max_concentration: float,
        num_positions: int
    ) -> str:
        """Assess overall risk level.

        Args:
            volatility: Portfolio volatility
            max_drawdown: Maximum drawdown
            max_concentration: Maximum position concentration
            num_positions: Number of positions

        Returns:
            Risk level: 'low', 'medium', 'high', or 'very_high'
        """
        risk_score = 0

        # Volatility
        if volatility > 0.40:  # 40%+ volatility
            risk_score += 3
        elif volatility > 0.25:
            risk_score += 2
        elif volatility > 0.15:
            risk_score += 1

        # Max drawdown
        if max_drawdown > 0.30:  # 30%+ drawdown
            risk_score += 3
        elif max_drawdown > 0.20:
            risk_score += 2
        elif max_drawdown > 0.10:
            risk_score += 1

        # Concentration
        if max_concentration > 0.30:  # 30%+ in single position
            risk_score += 2
        elif max_concentration > 0.20:
            risk_score += 1

        # Diversification
        if num_positions < 5:
            risk_score += 2
        elif num_positions < 10:
            risk_score += 1

        # Map to risk level
        if risk_score <= 2:
            return 'low'
        elif risk_score <= 4:
            return 'medium'
        elif risk_score <= 7:
            return 'high'
        else:
            return 'very_high'

    def should_rebalance(
        self,
        portfolio: Portfolio,
        current_prices: Dict[str, float],
        target_allocation: Dict[str, float]
    ) -> bool:
        """Check if portfolio should be rebalanced.

        Args:
            portfolio: Portfolio instance
            current_prices: Current prices
            target_allocation: Target allocation percentages

        Returns:
            True if rebalancing needed
        """
        current_allocation = portfolio.get_allocation(current_prices)
        threshold = self.config.get('portfolio.rebalancing.threshold', 0.05)

        for symbol, target_pct in target_allocation.items():
            current_pct = current_allocation.get(symbol, 0)
            drift = abs(current_pct - target_pct)

            if drift > threshold:
                logger.info(
                    f"Rebalancing needed for {symbol}: {current_pct:.1%} vs target {target_pct:.1%}"
                )
                return True

        return False


__all__ = ['RiskManager']
