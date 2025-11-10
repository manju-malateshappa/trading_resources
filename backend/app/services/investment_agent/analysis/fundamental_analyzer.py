"""Fundamental analysis module for stock evaluation."""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
from datetime import datetime

from ..utils.logger import logger
from ..utils.config_loader import config


class FundamentalAnalyzer:
    """Analyze fundamental metrics of stocks."""

    def __init__(self):
        """Initialize fundamental analyzer with configuration."""
        self.entry_criteria = config.get('strategy.entry', {})
        self.exit_criteria = config.get('strategy.exit', {})

    def analyze_stock(self, fundamentals: Dict, statements: Dict = None) -> Dict:
        """Perform comprehensive fundamental analysis.

        Args:
            fundamentals: Dictionary of fundamental metrics
            statements: Financial statements (optional)

        Returns:
            Analysis results with scores and signals
        """
        logger.info(f"Analyzing fundamentals for {fundamentals.get('symbol', 'Unknown')}")

        analysis = {
            'symbol': fundamentals.get('symbol'),
            'valuation_score': self._calculate_valuation_score(fundamentals),
            'growth_score': self._calculate_growth_score(fundamentals),
            'profitability_score': self._calculate_profitability_score(fundamentals),
            'financial_health_score': self._calculate_financial_health_score(fundamentals),
            'quality_score': self._calculate_quality_score(fundamentals),
            'momentum_score': self._calculate_momentum_score(fundamentals),
        }

        # Calculate overall score (weighted average)
        weights = {
            'valuation_score': 0.15,
            'growth_score': 0.30,  # Heavy weight on growth for high-growth strategy
            'profitability_score': 0.20,
            'financial_health_score': 0.20,
            'quality_score': 0.10,
            'momentum_score': 0.05,
        }

        overall_score = sum(
            analysis[key] * weight
            for key, weight in weights.items()
            if analysis[key] is not None
        )

        analysis['overall_score'] = overall_score
        analysis['buy_signal'] = self._generate_buy_signal(fundamentals, analysis)
        analysis['risk_level'] = self._assess_risk(fundamentals, analysis)
        analysis['growth_potential'] = self._estimate_growth_potential(fundamentals)

        return analysis

    def _calculate_valuation_score(self, data: Dict) -> Optional[float]:
        """Calculate valuation score (0-100).

        Lower multiples = higher score (more attractive valuation)
        """
        try:
            score = 50  # Base score

            # P/E ratio analysis
            pe = data.get('pe_ratio')
            if pe and pe > 0:
                if pe < 15:
                    score += 20
                elif pe < 20:
                    score += 10
                elif pe < 30:
                    score += 0
                elif pe < 50:
                    score -= 10
                else:
                    score -= 20

            # PEG ratio (P/E to Growth)
            peg = data.get('peg_ratio')
            if peg and peg > 0:
                if peg < 1.0:
                    score += 15  # Undervalued
                elif peg < 1.5:
                    score += 5
                elif peg < 2.0:
                    score -= 5
                else:
                    score -= 15  # Overvalued

            # Price to Book
            pb = data.get('price_to_book')
            if pb and pb > 0:
                if pb < 2:
                    score += 10
                elif pb < 5:
                    score += 0
                else:
                    score -= 10

            # Price to Sales
            ps = data.get('price_to_sales')
            if ps and ps > 0:
                if ps < 2:
                    score += 10
                elif ps < 5:
                    score += 0
                elif ps < 10:
                    score -= 5
                else:
                    score -= 15

            return max(0, min(100, score))

        except Exception as e:
            logger.error(f"Error calculating valuation score: {str(e)}")
            return None

    def _calculate_growth_score(self, data: Dict) -> Optional[float]:
        """Calculate growth score (0-100).

        Higher growth = higher score
        """
        try:
            score = 50  # Base score

            # Revenue growth
            rev_growth = data.get('revenue_growth')
            if rev_growth is not None:
                if rev_growth > 0.50:  # 50%+ growth
                    score += 30
                elif rev_growth > 0.30:  # 30%+ growth
                    score += 20
                elif rev_growth > 0.15:  # 15%+ growth
                    score += 10
                elif rev_growth > 0:
                    score += 0
                else:
                    score -= 30  # Declining revenue

            # Earnings growth
            earn_growth = data.get('earnings_growth')
            if earn_growth is not None:
                if earn_growth > 0.50:
                    score += 20
                elif earn_growth > 0.30:
                    score += 15
                elif earn_growth > 0.15:
                    score += 10
                elif earn_growth > 0:
                    score += 5
                else:
                    score -= 20

            return max(0, min(100, score))

        except Exception as e:
            logger.error(f"Error calculating growth score: {str(e)}")
            return None

    def _calculate_profitability_score(self, data: Dict) -> Optional[float]:
        """Calculate profitability score (0-100)."""
        try:
            score = 50

            # Profit margin
            profit_margin = data.get('profit_margin')
            if profit_margin is not None:
                if profit_margin > 0.20:  # 20%+ margin
                    score += 20
                elif profit_margin > 0.10:
                    score += 15
                elif profit_margin > 0.05:
                    score += 10
                elif profit_margin > 0:
                    score += 0
                else:
                    score -= 30  # Unprofitable

            # Operating margin
            op_margin = data.get('operating_margin')
            if op_margin is not None:
                if op_margin > 0.15:
                    score += 15
                elif op_margin > 0.10:
                    score += 10
                elif op_margin > 0:
                    score += 5

            # ROE (Return on Equity)
            roe = data.get('roe')
            if roe is not None:
                if roe > 0.20:  # 20%+ ROE
                    score += 15
                elif roe > 0.15:
                    score += 10
                elif roe > 0.10:
                    score += 5

            return max(0, min(100, score))

        except Exception as e:
            logger.error(f"Error calculating profitability score: {str(e)}")
            return None

    def _calculate_financial_health_score(self, data: Dict) -> Optional[float]:
        """Calculate financial health score (0-100)."""
        try:
            score = 50

            # Current ratio (liquidity)
            current_ratio = data.get('current_ratio')
            if current_ratio is not None:
                if current_ratio > 2.0:
                    score += 15
                elif current_ratio > 1.5:
                    score += 10
                elif current_ratio > 1.0:
                    score += 5
                else:
                    score -= 20  # Liquidity concerns

            # Debt to equity
            debt_to_equity = data.get('debt_to_equity')
            if debt_to_equity is not None:
                if debt_to_equity < 0.5:
                    score += 20  # Low debt
                elif debt_to_equity < 1.0:
                    score += 10
                elif debt_to_equity < 2.0:
                    score += 0
                else:
                    score -= 20  # High debt

            # Free cash flow
            fcf = data.get('free_cash_flow')
            if fcf is not None and fcf > 0:
                score += 15
            elif fcf is not None and fcf < 0:
                score -= 15

            return max(0, min(100, score))

        except Exception as e:
            logger.error(f"Error calculating financial health score: {str(e)}")
            return None

    def _calculate_quality_score(self, data: Dict) -> Optional[float]:
        """Calculate quality score based on market position and stability."""
        try:
            score = 50

            # Market cap (larger = more stable, but we want small/mid cap)
            market_cap = data.get('market_cap', 0)
            if 2_000_000_000 < market_cap < 10_000_000_000:  # $2B-$10B (mid-cap sweet spot)
                score += 15
            elif 300_000_000 < market_cap < 2_000_000_000:  # $300M-$2B (small-cap)
                score += 10
            elif market_cap > 10_000_000_000:  # Too large
                score -= 5

            # Institutional ownership (credibility)
            inst_own = data.get('institutional_ownership', 0)
            if 0.20 < inst_own < 0.80:  # Sweet spot
                score += 15
            elif 0.10 < inst_own < 0.90:
                score += 10

            # Insider ownership (alignment)
            insider_own = data.get('insider_ownership', 0)
            if insider_own > 0.10:  # 10%+ insider ownership
                score += 10
            elif insider_own > 0.05:
                score += 5

            # Analyst coverage
            recommendation = data.get('recommendation', '')
            if recommendation in ['buy', 'strong_buy']:
                score += 10
            elif recommendation in ['hold']:
                score += 0
            else:
                score -= 10

            return max(0, min(100, score))

        except Exception as e:
            logger.error(f"Error calculating quality score: {str(e)}")
            return None

    def _calculate_momentum_score(self, data: Dict) -> Optional[float]:
        """Calculate price momentum score."""
        try:
            score = 50

            current_price = data.get('current_price', 0)
            high_52w = data.get('52w_high', 0)
            low_52w = data.get('52w_low', 0)

            if current_price and high_52w and low_52w and high_52w > low_52w:
                # Calculate position in 52-week range
                range_position = (current_price - low_52w) / (high_52w - low_52w)

                if range_position > 0.80:  # Near highs
                    score += 20
                elif range_position > 0.60:
                    score += 10
                elif range_position < 0.30:  # Near lows (potential value)
                    score += 5

            return max(0, min(100, score))

        except Exception as e:
            logger.error(f"Error calculating momentum score: {str(e)}")
            return None

    def _generate_buy_signal(self, data: Dict, analysis: Dict) -> str:
        """Generate buy signal based on criteria.

        Returns:
            'strong_buy', 'buy', 'hold', 'sell', or 'strong_sell'
        """
        overall_score = analysis.get('overall_score', 0)
        growth_score = analysis.get('growth_score', 0)

        # Check minimum criteria from config
        min_revenue_growth = self.entry_criteria.get('min_revenue_growth', 0.15)
        max_pe = self.entry_criteria.get('max_pe_ratio', 30)
        min_margin = self.entry_criteria.get('min_profit_margin', 0.05)

        revenue_growth = data.get('revenue_growth', 0)
        pe_ratio = data.get('pe_ratio', 999)
        profit_margin = data.get('profit_margin', 0)

        # Check if meets minimum criteria
        meets_criteria = (
            revenue_growth >= min_revenue_growth and
            (pe_ratio is None or pe_ratio <= max_pe or pe_ratio < 0) and
            profit_margin >= min_margin
        )

        if not meets_criteria:
            return 'hold'

        # Generate signal based on overall score
        if overall_score >= 75 and growth_score >= 70:
            return 'strong_buy'
        elif overall_score >= 65:
            return 'buy'
        elif overall_score >= 50:
            return 'hold'
        elif overall_score >= 35:
            return 'sell'
        else:
            return 'strong_sell'

    def _assess_risk(self, data: Dict, analysis: Dict) -> str:
        """Assess risk level.

        Returns:
            'low', 'medium', 'high', or 'very_high'
        """
        risk_factors = 0

        # Financial health
        if analysis.get('financial_health_score', 50) < 40:
            risk_factors += 2

        # Debt levels
        debt_to_equity = data.get('debt_to_equity', 0)
        if debt_to_equity > 2.0:
            risk_factors += 2

        # Profitability
        profit_margin = data.get('profit_margin', 0)
        if profit_margin < 0:
            risk_factors += 2
        elif profit_margin < 0.05:
            risk_factors += 1

        # Valuation
        pe_ratio = data.get('pe_ratio')
        if pe_ratio and pe_ratio > 50:
            risk_factors += 1

        # Beta (volatility)
        beta = data.get('beta', 1.0)
        if beta and beta > 1.5:
            risk_factors += 1

        # Market cap (smaller = riskier)
        market_cap = data.get('market_cap', 0)
        if market_cap < 300_000_000:
            risk_factors += 2
        elif market_cap < 1_000_000_000:
            risk_factors += 1

        # Map risk factors to risk level
        if risk_factors <= 2:
            return 'low'
        elif risk_factors <= 4:
            return 'medium'
        elif risk_factors <= 6:
            return 'high'
        else:
            return 'very_high'

    def _estimate_growth_potential(self, data: Dict) -> Dict:
        """Estimate potential return over 1-2 years.

        Returns:
            Dictionary with conservative, expected, and optimistic returns
        """
        # Simple model based on historical growth and valuation
        revenue_growth = data.get('revenue_growth', 0)
        pe_ratio = data.get('pe_ratio', 20)
        target_mean = data.get('target_mean')
        current_price = data.get('current_price')

        # Calculate potential based on analyst targets
        analyst_upside = 0
        if target_mean and current_price and current_price > 0:
            analyst_upside = (target_mean - current_price) / current_price

        # Estimate based on growth rate and multiple expansion
        growth_based_return = revenue_growth * 1.5 if revenue_growth > 0 else 0

        # Conservative: Lower of analyst target or growth-based
        conservative = min(analyst_upside, growth_based_return) if analyst_upside > 0 else growth_based_return * 0.5

        # Expected: Average of both
        expected = (analyst_upside + growth_based_return) / 2 if analyst_upside > 0 else growth_based_return

        # Optimistic: Higher + some multiple expansion
        optimistic = max(analyst_upside, growth_based_return) * 1.5 if analyst_upside > 0 else growth_based_return * 2

        return {
            'conservative_1y': max(0, conservative),
            'expected_1y': max(0, expected),
            'optimistic_1y': max(0, optimistic),
            'conservative_2y': max(0, conservative * 1.5),
            'expected_2y': max(0, expected * 1.8),
            'optimistic_2y': max(0, optimistic * 2.0),
            'analyst_target_upside': max(0, analyst_upside) if analyst_upside else None,
        }

    def check_exit_signals(self, fundamentals: Dict, statements: Dict = None) -> List[str]:
        """Check for fundamental deterioration signals.

        Args:
            fundamentals: Current fundamental data
            statements: Financial statements

        Returns:
            List of exit signals
        """
        signals = []

        # Revenue decline
        revenue_growth = fundamentals.get('revenue_growth')
        if revenue_growth is not None and revenue_growth < -0.10:  # 10% decline
            signals.append(f"Revenue declining: {revenue_growth:.1%}")

        # Margin compression
        profit_margin = fundamentals.get('profit_margin', 0)
        if profit_margin < 0.02:  # Below 2% margin
            signals.append(f"Low profit margin: {profit_margin:.1%}")

        # Deteriorating financial health
        current_ratio = fundamentals.get('current_ratio', 0)
        if current_ratio < 1.0:
            signals.append(f"Liquidity concern: Current ratio {current_ratio:.2f}")

        # High debt
        debt_to_equity = fundamentals.get('debt_to_equity')
        if debt_to_equity and debt_to_equity > 3.0:
            signals.append(f"High debt: D/E ratio {debt_to_equity:.2f}")

        # Analyst downgrades
        recommendation = fundamentals.get('recommendation', '')
        if recommendation in ['sell', 'strong_sell']:
            signals.append(f"Analyst rating: {recommendation}")

        return signals


__all__ = ['FundamentalAnalyzer']
