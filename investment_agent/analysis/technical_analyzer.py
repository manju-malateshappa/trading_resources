"""Technical analysis module for stock evaluation."""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
import pandas_ta as ta

from ..utils.logger import logger
from ..utils.config_loader import config


class TechnicalAnalyzer:
    """Perform technical analysis on stock price data."""

    def __init__(self):
        """Initialize technical analyzer."""
        self.config = config

    def analyze_stock(self, df: pd.DataFrame, symbol: str = "") -> Dict:
        """Perform comprehensive technical analysis.

        Args:
            df: DataFrame with OHLCV data
            symbol: Stock ticker symbol

        Returns:
            Dictionary with technical analysis results
        """
        if df.empty:
            logger.warning(f"Empty DataFrame for {symbol}")
            return {}

        logger.info(f"Performing technical analysis for {symbol}")

        # Calculate all indicators
        df = self._calculate_indicators(df)

        # Analyze current state
        latest = df.iloc[-1]

        analysis = {
            'symbol': symbol,
            'current_price': latest.get('Close', 0),
            'volume': latest.get('Volume', 0),

            # Trend indicators
            'trend': self._determine_trend(df),
            'trend_strength': self._calculate_trend_strength(df),

            # Momentum indicators
            'rsi': latest.get('RSI_14', 50),
            'rsi_signal': self._interpret_rsi(latest.get('RSI_14', 50)),
            'macd': latest.get('MACD_12_26_9', 0),
            'macd_signal': latest.get('MACDs_12_26_9', 0),
            'macd_histogram': latest.get('MACDh_12_26_9', 0),

            # Moving averages
            'sma_20': latest.get('SMA_20', 0),
            'sma_50': latest.get('SMA_50', 0),
            'sma_200': latest.get('SMA_200', 0),
            'price_vs_sma20': self._price_vs_ma(latest.get('Close'), latest.get('SMA_20')),
            'price_vs_sma50': self._price_vs_ma(latest.get('Close'), latest.get('SMA_50')),
            'price_vs_sma200': self._price_vs_ma(latest.get('Close'), latest.get('SMA_200')),

            # Volatility indicators
            'bb_upper': latest.get('BBU_20_2.0', 0),
            'bb_middle': latest.get('BBM_20_2.0', 0),
            'bb_lower': latest.get('BBL_20_2.0', 0),
            'bb_position': self._bb_position(latest),
            'atr': latest.get('ATR_14', 0),

            # Volume analysis
            'volume_trend': self._analyze_volume(df),
            'volume_vs_avg': self._volume_vs_average(df),

            # Support/Resistance
            'support_levels': self._find_support_levels(df),
            'resistance_levels': self._find_resistance_levels(df),

            # Signals
            'buy_signals': self._generate_buy_signals(df),
            'sell_signals': self._generate_sell_signals(df),
            'overall_signal': self._overall_technical_signal(df),
            'signal_strength': self._calculate_signal_strength(df),
        }

        return analysis

    def _calculate_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate all technical indicators.

        Args:
            df: DataFrame with OHLCV data

        Returns:
            DataFrame with added technical indicators
        """
        # Make a copy to avoid modifying original
        df = df.copy()

        # Moving Averages
        df['SMA_20'] = ta.sma(df['Close'], length=20)
        df['SMA_50'] = ta.sma(df['Close'], length=50)
        df['SMA_200'] = ta.sma(df['Close'], length=200)
        df['EMA_12'] = ta.ema(df['Close'], length=12)
        df['EMA_26'] = ta.ema(df['Close'], length=26)

        # RSI (Relative Strength Index)
        df['RSI_14'] = ta.rsi(df['Close'], length=14)

        # MACD (Moving Average Convergence Divergence)
        macd = ta.macd(df['Close'], fast=12, slow=26, signal=9)
        if macd is not None:
            df = pd.concat([df, macd], axis=1)

        # Bollinger Bands
        bbands = ta.bbands(df['Close'], length=20, std=2)
        if bbands is not None:
            df = pd.concat([df, bbands], axis=1)

        # ATR (Average True Range)
        df['ATR_14'] = ta.atr(df['High'], df['Low'], df['Close'], length=14)

        # ADX (Average Directional Index)
        adx = ta.adx(df['High'], df['Low'], df['Close'], length=14)
        if adx is not None:
            df = pd.concat([df, adx], axis=1)

        # Stochastic Oscillator
        stoch = ta.stoch(df['High'], df['Low'], df['Close'])
        if stoch is not None:
            df = pd.concat([df, stoch], axis=1)

        # Volume indicators
        df['Volume_SMA_20'] = ta.sma(df['Volume'], length=20)

        # OBV (On-Balance Volume)
        df['OBV'] = ta.obv(df['Close'], df['Volume'])

        return df

    def _determine_trend(self, df: pd.DataFrame) -> str:
        """Determine current price trend.

        Returns:
            'strong_uptrend', 'uptrend', 'sideways', 'downtrend', or 'strong_downtrend'
        """
        latest = df.iloc[-1]
        close = latest.get('Close', 0)
        sma_20 = latest.get('SMA_20', 0)
        sma_50 = latest.get('SMA_50', 0)
        sma_200 = latest.get('SMA_200', 0)

        # Count bullish conditions
        bullish_count = 0
        total_conditions = 0

        if sma_20 and sma_50:
            total_conditions += 1
            if sma_20 > sma_50:
                bullish_count += 1

        if sma_50 and sma_200:
            total_conditions += 1
            if sma_50 > sma_200:
                bullish_count += 1

        if close and sma_20:
            total_conditions += 1
            if close > sma_20:
                bullish_count += 1

        if close and sma_50:
            total_conditions += 1
            if close > sma_50:
                bullish_count += 1

        if total_conditions == 0:
            return 'unknown'

        ratio = bullish_count / total_conditions

        if ratio >= 0.75:
            return 'strong_uptrend'
        elif ratio >= 0.50:
            return 'uptrend'
        elif ratio >= 0.25:
            return 'sideways'
        elif ratio > 0:
            return 'downtrend'
        else:
            return 'strong_downtrend'

    def _calculate_trend_strength(self, df: pd.DataFrame) -> Optional[float]:
        """Calculate trend strength using ADX.

        Returns:
            ADX value (0-100), where >25 indicates strong trend
        """
        latest = df.iloc[-1]
        adx = latest.get('ADX_14')
        return adx

    def _interpret_rsi(self, rsi: Optional[float]) -> str:
        """Interpret RSI value.

        Returns:
            'oversold', 'neutral', or 'overbought'
        """
        if rsi is None:
            return 'unknown'

        if rsi < 30:
            return 'oversold'
        elif rsi > 70:
            return 'overbought'
        else:
            return 'neutral'

    def _price_vs_ma(self, price: float, ma: float) -> Optional[float]:
        """Calculate price position relative to moving average.

        Returns:
            Percentage difference (positive = above MA)
        """
        if not price or not ma or ma == 0:
            return None

        return (price - ma) / ma

    def _bb_position(self, latest: pd.Series) -> Optional[float]:
        """Calculate position within Bollinger Bands.

        Returns:
            Value 0-1 (0 = at lower band, 1 = at upper band)
        """
        close = latest.get('Close')
        bb_upper = latest.get('BBU_20_2.0')
        bb_lower = latest.get('BBL_20_2.0')

        if not all([close, bb_upper, bb_lower]) or bb_upper == bb_lower:
            return None

        position = (close - bb_lower) / (bb_upper - bb_lower)
        return max(0, min(1, position))

    def _analyze_volume(self, df: pd.DataFrame) -> str:
        """Analyze volume trend.

        Returns:
            'increasing', 'decreasing', or 'stable'
        """
        if len(df) < 20:
            return 'unknown'

        recent_volume = df['Volume'].iloc[-10:].mean()
        older_volume = df['Volume'].iloc[-30:-10].mean()

        if older_volume == 0:
            return 'unknown'

        change = (recent_volume - older_volume) / older_volume

        if change > 0.20:
            return 'increasing'
        elif change < -0.20:
            return 'decreasing'
        else:
            return 'stable'

    def _volume_vs_average(self, df: pd.DataFrame) -> Optional[float]:
        """Compare current volume to average.

        Returns:
            Ratio of current volume to 20-day average
        """
        latest = df.iloc[-1]
        current_volume = latest.get('Volume', 0)
        avg_volume = latest.get('Volume_SMA_20', 0)

        if avg_volume and avg_volume > 0:
            return current_volume / avg_volume

        return None

    def _find_support_levels(self, df: pd.DataFrame, num_levels: int = 3) -> List[float]:
        """Find support levels using local minima.

        Args:
            df: Price data
            num_levels: Number of support levels to find

        Returns:
            List of support price levels
        """
        if len(df) < 50:
            return []

        # Look at recent lows
        recent_df = df.iloc[-100:] if len(df) >= 100 else df

        # Find local minima
        lows = recent_df['Low'].values
        support_levels = []

        for i in range(2, len(lows) - 2):
            if (lows[i] < lows[i-1] and lows[i] < lows[i-2] and
                lows[i] < lows[i+1] and lows[i] < lows[i+2]):
                support_levels.append(lows[i])

        # Return the strongest (most recent and tested) support levels
        support_levels = sorted(set(support_levels), reverse=True)
        return support_levels[:num_levels]

    def _find_resistance_levels(self, df: pd.DataFrame, num_levels: int = 3) -> List[float]:
        """Find resistance levels using local maxima.

        Args:
            df: Price data
            num_levels: Number of resistance levels to find

        Returns:
            List of resistance price levels
        """
        if len(df) < 50:
            return []

        # Look at recent highs
        recent_df = df.iloc[-100:] if len(df) >= 100 else df

        # Find local maxima
        highs = recent_df['High'].values
        resistance_levels = []

        for i in range(2, len(highs) - 2):
            if (highs[i] > highs[i-1] and highs[i] > highs[i-2] and
                highs[i] > highs[i+1] and highs[i] > highs[i+2]):
                resistance_levels.append(highs[i])

        # Return the strongest resistance levels
        resistance_levels = sorted(set(resistance_levels))
        return resistance_levels[:num_levels]

    def _generate_buy_signals(self, df: pd.DataFrame) -> List[str]:
        """Generate buy signals based on technical indicators.

        Returns:
            List of buy signal descriptions
        """
        signals = []
        latest = df.iloc[-1]
        previous = df.iloc[-2] if len(df) > 1 else latest

        # RSI oversold
        rsi = latest.get('RSI_14')
        if rsi and rsi < 35:
            signals.append(f"RSI oversold ({rsi:.1f})")

        # MACD bullish crossover
        macd = latest.get('MACD_12_26_9')
        macd_signal = latest.get('MACDs_12_26_9')
        prev_macd = previous.get('MACD_12_26_9')
        prev_signal = previous.get('MACDs_12_26_9')

        if all([macd, macd_signal, prev_macd, prev_signal]):
            if macd > macd_signal and prev_macd <= prev_signal:
                signals.append("MACD bullish crossover")

        # Golden cross (50-day crosses above 200-day)
        sma_50 = latest.get('SMA_50')
        sma_200 = latest.get('SMA_200')
        prev_sma_50 = previous.get('SMA_50')
        prev_sma_200 = previous.get('SMA_200')

        if all([sma_50, sma_200, prev_sma_50, prev_sma_200]):
            if sma_50 > sma_200 and prev_sma_50 <= prev_sma_200:
                signals.append("Golden cross (SMA50 > SMA200)")

        # Price near lower Bollinger Band
        bb_position = self._bb_position(latest)
        if bb_position is not None and bb_position < 0.2:
            signals.append("Price near lower Bollinger Band")

        # Volume spike with price increase
        volume_ratio = self._volume_vs_average(df)
        price_change = (latest.get('Close', 0) - previous.get('Close', 1)) / previous.get('Close', 1)

        if volume_ratio and volume_ratio > 1.5 and price_change > 0.02:
            signals.append("High volume breakout")

        return signals

    def _generate_sell_signals(self, df: pd.DataFrame) -> List[str]:
        """Generate sell signals based on technical indicators.

        Returns:
            List of sell signal descriptions
        """
        signals = []
        latest = df.iloc[-1]
        previous = df.iloc[-2] if len(df) > 1 else latest

        # RSI overbought
        rsi = latest.get('RSI_14')
        if rsi and rsi > 70:
            signals.append(f"RSI overbought ({rsi:.1f})")

        # MACD bearish crossover
        macd = latest.get('MACD_12_26_9')
        macd_signal = latest.get('MACDs_12_26_9')
        prev_macd = previous.get('MACD_12_26_9')
        prev_signal = previous.get('MACDs_12_26_9')

        if all([macd, macd_signal, prev_macd, prev_signal]):
            if macd < macd_signal and prev_macd >= prev_signal:
                signals.append("MACD bearish crossover")

        # Death cross (50-day crosses below 200-day)
        sma_50 = latest.get('SMA_50')
        sma_200 = latest.get('SMA_200')
        prev_sma_50 = previous.get('SMA_50')
        prev_sma_200 = previous.get('SMA_200')

        if all([sma_50, sma_200, prev_sma_50, prev_sma_200]):
            if sma_50 < sma_200 and prev_sma_50 >= prev_sma_200:
                signals.append("Death cross (SMA50 < SMA200)")

        # Price near upper Bollinger Band
        bb_position = self._bb_position(latest)
        if bb_position is not None and bb_position > 0.8:
            signals.append("Price near upper Bollinger Band")

        # Breaking below key support
        close = latest.get('Close', 0)
        sma_200 = latest.get('SMA_200', 0)
        if close and sma_200 and close < sma_200:
            deviation = (sma_200 - close) / sma_200
            if deviation > 0.05:  # 5% below 200-day MA
                signals.append("Price significantly below 200-day MA")

        return signals

    def _overall_technical_signal(self, df: pd.DataFrame) -> str:
        """Generate overall technical signal.

        Returns:
            'strong_buy', 'buy', 'hold', 'sell', or 'strong_sell'
        """
        buy_signals = self._generate_buy_signals(df)
        sell_signals = self._generate_sell_signals(df)
        trend = self._determine_trend(df)

        # Calculate score
        score = len(buy_signals) - len(sell_signals)

        # Adjust for trend
        if trend == 'strong_uptrend':
            score += 2
        elif trend == 'uptrend':
            score += 1
        elif trend == 'downtrend':
            score -= 1
        elif trend == 'strong_downtrend':
            score -= 2

        # Generate signal
        if score >= 3:
            return 'strong_buy'
        elif score >= 1:
            return 'buy'
        elif score >= -1:
            return 'hold'
        elif score >= -3:
            return 'sell'
        else:
            return 'strong_sell'

    def _calculate_signal_strength(self, df: pd.DataFrame) -> float:
        """Calculate strength of the technical signal (0-100).

        Returns:
            Signal strength score
        """
        score = 50  # Base score

        # Trend contribution
        trend = self._determine_trend(df)
        trend_scores = {
            'strong_uptrend': 20,
            'uptrend': 10,
            'sideways': 0,
            'downtrend': -10,
            'strong_downtrend': -20,
        }
        score += trend_scores.get(trend, 0)

        # Signal agreement
        buy_signals = len(self._generate_buy_signals(df))
        sell_signals = len(self._generate_sell_signals(df))
        score += (buy_signals - sell_signals) * 5

        # Volume confirmation
        volume_trend = self._analyze_volume(df)
        if volume_trend == 'increasing' and trend in ['uptrend', 'strong_uptrend']:
            score += 10
        elif volume_trend == 'increasing' and trend in ['downtrend', 'strong_downtrend']:
            score -= 10

        return max(0, min(100, score))


__all__ = ['TechnicalAnalyzer']
