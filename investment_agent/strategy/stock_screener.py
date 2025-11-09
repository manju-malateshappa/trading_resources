"""Stock screening module for finding high-growth investment opportunities."""

import pandas as pd
import numpy as np
from typing import List, Dict, Optional
from datetime import datetime
import time

from ..data.data_fetcher import DataFetcher
from ..analysis.fundamental_analyzer import FundamentalAnalyzer
from ..analysis.technical_analyzer import TechnicalAnalyzer
from ..utils.logger import logger
from ..utils.config_loader import config


class StockScreener:
    """Screen stocks for high-growth investment opportunities."""

    def __init__(self):
        """Initialize stock screener."""
        self.data_fetcher = DataFetcher()
        self.fundamental_analyzer = FundamentalAnalyzer()
        self.technical_analyzer = TechnicalAnalyzer()
        self.config = config

    def screen_for_opportunities(
        self,
        markets: List[str] = None,
        min_score: float = 65.0,
        max_results: int = 50
    ) -> pd.DataFrame:
        """Screen stocks for high-growth opportunities.

        Args:
            markets: List of markets to screen (TSX, TSXV, NASDAQ, NYSE)
            min_score: Minimum overall score (0-100)
            max_results: Maximum number of results to return

        Returns:
            DataFrame with screened stocks and their analysis
        """
        if markets is None:
            markets = self.config.get('screening.markets', ['TSX', 'NASDAQ'])

        logger.info(f"Starting stock screening for markets: {markets}")

        all_candidates = []

        for market in markets:
            logger.info(f"Screening {market} market...")
            candidates = self._screen_market(market)
            all_candidates.extend(candidates)

        # Convert to DataFrame
        if not all_candidates:
            logger.warning("No candidates found")
            return pd.DataFrame()

        df = pd.DataFrame(all_candidates)

        # Filter by minimum score
        df = df[df['overall_score'] >= min_score]

        # Sort by overall score
        df = df.sort_values('overall_score', ascending=False)

        # Limit results
        df = df.head(max_results)

        logger.info(f"Found {len(df)} high-quality opportunities")

        return df

    def _screen_market(self, market: str) -> List[Dict]:
        """Screen a specific market for opportunities.

        Args:
            market: Market to screen (TSX, TSXV, NASDAQ, NYSE)

        Returns:
            List of candidate stocks with analysis
        """
        # Get list of stocks in the market cap range
        min_cap = self.config.get('screening.emerging_criteria.min_market_cap', 100_000_000)
        max_cap = self.config.get('screening.emerging_criteria.max_market_cap', 10_000_000_000)

        tickers = self.data_fetcher.get_market_cap_range_stocks(
            min_cap=min_cap,
            max_cap=max_cap,
            market=market
        )

        logger.info(f"Analyzing {len(tickers)} tickers from {market}")

        candidates = []

        for ticker in tickers:
            try:
                logger.info(f"Analyzing {ticker}...")

                # Fetch data
                fundamentals = self.data_fetcher.get_fundamental_data(ticker)
                if not fundamentals:
                    logger.warning(f"No fundamental data for {ticker}")
                    continue

                # Apply initial filters
                if not self._passes_initial_filters(fundamentals):
                    logger.debug(f"{ticker} failed initial filters")
                    continue

                # Perform fundamental analysis
                fund_analysis = self.fundamental_analyzer.analyze_stock(fundamentals)

                # Fetch price data for technical analysis
                price_data = self.data_fetcher.get_stock_data(ticker, period="1y", interval="1d")
                if price_data.empty:
                    logger.warning(f"No price data for {ticker}")
                    continue

                # Perform technical analysis
                tech_analysis = self.technical_analyzer.analyze_stock(price_data, ticker)

                # Combine analyses
                combined = self._combine_analyses(fundamentals, fund_analysis, tech_analysis)

                if combined and combined['overall_score'] >= 50:
                    candidates.append(combined)
                    logger.info(f"{ticker}: Score={combined['overall_score']:.1f}")

                # Rate limiting
                time.sleep(0.5)

            except Exception as e:
                logger.error(f"Error analyzing {ticker}: {str(e)}")
                continue

        return candidates

    def _passes_initial_filters(self, fundamentals: Dict) -> bool:
        """Apply initial filters to quickly eliminate unsuitable stocks.

        Args:
            fundamentals: Fundamental data

        Returns:
            True if passes all filters
        """
        criteria = self.config.get('screening.emerging_criteria', {})

        # Market cap filter
        market_cap = fundamentals.get('market_cap', 0)
        min_cap = criteria.get('min_market_cap', 100_000_000)
        max_cap = criteria.get('max_market_cap', 10_000_000_000)

        if not (min_cap <= market_cap <= max_cap):
            return False

        # Volume filter
        avg_volume = fundamentals.get('avg_volume', 0)
        min_volume = criteria.get('min_avg_volume', 50000)

        if avg_volume < min_volume:
            return False

        # Price filter
        price = fundamentals.get('current_price', 0)
        min_price = criteria.get('min_price', 1.0)
        max_price = criteria.get('max_price', 100.0)

        if not (min_price <= price <= max_price):
            return False

        # Minimum revenue growth
        revenue_growth = fundamentals.get('revenue_growth')
        min_growth = self.config.get('strategy.entry.min_revenue_growth', 0.15)

        if revenue_growth is None or revenue_growth < min_growth:
            return False

        # Minimum profit margin (or allow unprofitable if high growth)
        profit_margin = fundamentals.get('profit_margin')
        min_margin = self.config.get('strategy.entry.min_profit_margin', 0.05)

        # Allow unprofitable companies if they have very high revenue growth
        if profit_margin is not None and profit_margin < min_margin:
            if revenue_growth is None or revenue_growth < 0.50:  # Must have 50%+ growth if unprofitable
                return False

        return True

    def _combine_analyses(
        self,
        fundamentals: Dict,
        fund_analysis: Dict,
        tech_analysis: Dict
    ) -> Dict:
        """Combine fundamental and technical analyses.

        Args:
            fundamentals: Raw fundamental data
            fund_analysis: Fundamental analysis results
            tech_analysis: Technical analysis results

        Returns:
            Combined analysis with overall score and recommendation
        """
        # Calculate weighted overall score
        # Growth stocks: Weight fundamentals more heavily, but confirm with technicals
        fundamental_weight = 0.70
        technical_weight = 0.30

        fund_score = fund_analysis.get('overall_score', 0)
        tech_signal_strength = tech_analysis.get('signal_strength', 50)

        overall_score = (fund_score * fundamental_weight +
                        tech_signal_strength * technical_weight)

        # Combine signals
        fund_signal = fund_analysis.get('buy_signal', 'hold')
        tech_signal = tech_analysis.get('overall_signal', 'hold')

        # Determine final recommendation
        recommendation = self._determine_recommendation(fund_signal, tech_signal, overall_score)

        # Estimate potential return
        growth_potential = fund_analysis.get('growth_potential', {})

        return {
            'symbol': fundamentals.get('symbol'),
            'name': fundamentals.get('name'),
            'sector': fundamentals.get('sector'),
            'industry': fundamentals.get('industry'),

            # Key metrics
            'current_price': fundamentals.get('current_price'),
            'market_cap': fundamentals.get('market_cap'),
            'pe_ratio': fundamentals.get('pe_ratio'),
            'revenue_growth': fundamentals.get('revenue_growth'),
            'profit_margin': fundamentals.get('profit_margin'),

            # Scores
            'overall_score': overall_score,
            'fundamental_score': fund_score,
            'technical_score': tech_signal_strength,
            'growth_score': fund_analysis.get('growth_score'),
            'valuation_score': fund_analysis.get('valuation_score'),
            'profitability_score': fund_analysis.get('profitability_score'),
            'financial_health_score': fund_analysis.get('financial_health_score'),

            # Signals
            'recommendation': recommendation,
            'fundamental_signal': fund_signal,
            'technical_signal': tech_signal,
            'trend': tech_analysis.get('trend'),
            'rsi': tech_analysis.get('rsi'),

            # Potential
            'expected_return_1y': growth_potential.get('expected_1y', 0),
            'expected_return_2y': growth_potential.get('expected_2y', 0),
            'optimistic_return_2y': growth_potential.get('optimistic_2y', 0),

            # Risk
            'risk_level': fund_analysis.get('risk_level'),
            'beta': fundamentals.get('beta'),

            # Technical indicators
            'buy_signals': len(tech_analysis.get('buy_signals', [])),
            'sell_signals': len(tech_analysis.get('sell_signals', [])),

            # Additional info
            'analyst_recommendation': fundamentals.get('recommendation'),
            'target_upside': growth_potential.get('analyst_target_upside'),

            'screened_date': datetime.now().strftime('%Y-%m-%d'),
        }

    def _determine_recommendation(
        self,
        fund_signal: str,
        tech_signal: str,
        overall_score: float
    ) -> str:
        """Determine final recommendation combining signals.

        Args:
            fund_signal: Fundamental signal
            tech_signal: Technical signal
            overall_score: Overall score (0-100)

        Returns:
            Final recommendation
        """
        # Convert signals to numeric scores
        signal_map = {
            'strong_buy': 2,
            'buy': 1,
            'hold': 0,
            'sell': -1,
            'strong_sell': -2
        }

        fund_score = signal_map.get(fund_signal, 0)
        tech_score = signal_map.get(tech_signal, 0)

        # Weighted average (fundamentals weighted more)
        combined_signal = fund_score * 0.7 + tech_score * 0.3

        # Adjust based on overall score
        if overall_score >= 80:
            combined_signal += 0.5
        elif overall_score < 50:
            combined_signal -= 0.5

        # Map back to recommendation
        if combined_signal >= 1.5:
            return 'strong_buy'
        elif combined_signal >= 0.5:
            return 'buy'
        elif combined_signal >= -0.5:
            return 'hold'
        elif combined_signal >= -1.5:
            return 'sell'
        else:
            return 'strong_sell'

    def screen_specific_sectors(self, sectors: List[str]) -> pd.DataFrame:
        """Screen specific sectors for opportunities.

        Args:
            sectors: List of sectors to screen

        Returns:
            DataFrame with opportunities in specified sectors
        """
        logger.info(f"Screening sectors: {sectors}")

        results = self.screen_for_opportunities()

        if results.empty:
            return results

        # Filter by sectors
        results = results[results['sector'].isin(sectors)]

        return results

    def find_breakout_candidates(self) -> pd.DataFrame:
        """Find stocks showing technical breakout patterns.

        Returns:
            DataFrame with breakout candidates
        """
        logger.info("Searching for breakout candidates...")

        results = self.screen_for_opportunities(min_score=60)

        if results.empty:
            return results

        # Filter for strong technical signals
        breakouts = results[
            (results['technical_signal'].isin(['buy', 'strong_buy'])) &
            (results['trend'].isin(['uptrend', 'strong_uptrend'])) &
            (results['buy_signals'] >= 2)
        ]

        return breakouts.sort_values('technical_score', ascending=False)

    def find_value_opportunities(self) -> pd.DataFrame:
        """Find undervalued stocks with high growth potential.

        Returns:
            DataFrame with value opportunities
        """
        logger.info("Searching for value opportunities...")

        results = self.screen_for_opportunities(min_score=60)

        if results.empty:
            return results

        # Filter for high growth but reasonable valuation
        value_stocks = results[
            (results['growth_score'] >= 70) &
            (results['valuation_score'] >= 60) &
            (results['pe_ratio'] <= 30)
        ]

        return value_stocks.sort_values('overall_score', ascending=False)

    def daily_scan(self) -> Dict[str, pd.DataFrame]:
        """Perform daily stock scan.

        Returns:
            Dictionary with different categories of opportunities
        """
        logger.info("=" * 50)
        logger.info("DAILY STOCK SCAN")
        logger.info("=" * 50)

        results = {
            'top_opportunities': self.screen_for_opportunities(min_score=70, max_results=20),
            'breakout_candidates': self.find_breakout_candidates(),
            'value_opportunities': self.find_value_opportunities(),
        }

        # Log summary
        for category, df in results.items():
            logger.info(f"{category}: {len(df)} stocks found")

        return results

    def weekly_scan(self) -> pd.DataFrame:
        """Perform comprehensive weekly scan.

        Returns:
            DataFrame with all opportunities
        """
        logger.info("=" * 50)
        logger.info("WEEKLY COMPREHENSIVE SCAN")
        logger.info("=" * 50)

        results = self.screen_for_opportunities(min_score=65, max_results=100)

        return results

    def screen_ai_companies(
        self,
        market: str = None,
        min_score: float = 65.0
    ) -> pd.DataFrame:
        """Screen AI companies specifically.

        Args:
            market: Market filter ('USA', 'CANADA', 'INDIA', or None for all)
            min_score: Minimum overall score

        Returns:
            DataFrame with AI company opportunities
        """
        logger.info(f"Screening AI companies for market: {market or 'ALL'}")

        # Get AI company symbols
        ai_symbols = self.data_fetcher.get_ai_companies(market=market)

        logger.info(f"Analyzing {len(ai_symbols)} AI companies...")

        all_candidates = []

        for symbol in ai_symbols:
            try:
                logger.info(f"Analyzing AI company: {symbol}...")

                # Fetch data
                fundamentals = self.data_fetcher.get_fundamental_data(symbol)
                if not fundamentals:
                    logger.warning(f"No fundamental data for {symbol}")
                    continue

                # Perform fundamental analysis
                fund_analysis = self.fundamental_analyzer.analyze_stock(fundamentals)

                # Fetch price data for technical analysis
                price_data = self.data_fetcher.get_stock_data(symbol, period="1y", interval="1d")
                if price_data.empty:
                    logger.warning(f"No price data for {symbol}")
                    continue

                # Perform technical analysis
                tech_analysis = self.technical_analyzer.analyze_stock(price_data, symbol)

                # Combine analyses
                combined = self._combine_analyses(fundamentals, fund_analysis, tech_analysis)

                if combined and combined['overall_score'] >= min_score:
                    all_candidates.append(combined)
                    logger.info(f"{symbol}: Score={combined['overall_score']:.1f}")

                # Rate limiting
                time.sleep(0.5)

            except Exception as e:
                logger.error(f"Error analyzing {symbol}: {str(e)}")
                continue

        if not all_candidates:
            logger.warning("No AI company candidates found")
            return pd.DataFrame()

        df = pd.DataFrame(all_candidates)
        df = df.sort_values('overall_score', ascending=False)

        logger.info(f"Found {len(df)} AI companies meeting criteria")

        return df

    def screen_sector(
        self,
        sector: str,
        market: str = None,
        min_score: float = 65.0
    ) -> pd.DataFrame:
        """Screen specific sector for opportunities.

        Args:
            sector: Sector name (e.g., 'Fintech', 'Cloud Computing', 'EV & Clean Energy')
            market: Market filter ('USA', 'CANADA', 'INDIA', or None for all)
            min_score: Minimum overall score

        Returns:
            DataFrame with sector opportunities
        """
        logger.info(f"Screening {sector} sector for market: {market or 'ALL'}")

        # Get sector company symbols
        sector_symbols = self.data_fetcher.get_sector_companies(sector, market=market)

        if not sector_symbols:
            logger.warning(f"No companies found for sector: {sector}")
            return pd.DataFrame()

        logger.info(f"Analyzing {len(sector_symbols)} companies in {sector}...")

        all_candidates = []

        for symbol in sector_symbols:
            try:
                logger.info(f"Analyzing {symbol}...")

                # Fetch data
                fundamentals = self.data_fetcher.get_fundamental_data(symbol)
                if not fundamentals:
                    logger.warning(f"No fundamental data for {symbol}")
                    continue

                # Perform fundamental analysis
                fund_analysis = self.fundamental_analyzer.analyze_stock(fundamentals)

                # Fetch price data for technical analysis
                price_data = self.data_fetcher.get_stock_data(symbol, period="1y", interval="1d")
                if price_data.empty:
                    logger.warning(f"No price data for {symbol}")
                    continue

                # Perform technical analysis
                tech_analysis = self.technical_analyzer.analyze_stock(price_data, symbol)

                # Combine analyses
                combined = self._combine_analyses(fundamentals, fund_analysis, tech_analysis)

                if combined and combined['overall_score'] >= min_score:
                    all_candidates.append(combined)
                    logger.info(f"{symbol}: Score={combined['overall_score']:.1f}")

                # Rate limiting
                time.sleep(0.5)

            except Exception as e:
                logger.error(f"Error analyzing {symbol}: {str(e)}")
                continue

        if not all_candidates:
            logger.warning(f"No candidates found in {sector}")
            return pd.DataFrame()

        df = pd.DataFrame(all_candidates)
        df = df.sort_values('overall_score', ascending=False)

        logger.info(f"Found {len(df)} companies in {sector} meeting criteria")

        return df

    def screen_indian_market(
        self,
        min_score: float = 65.0,
        max_results: int = 50
    ) -> pd.DataFrame:
        """Screen Indian market (NSE) for opportunities.

        Args:
            min_score: Minimum overall score
            max_results: Maximum number of results

        Returns:
            DataFrame with Indian market opportunities
        """
        logger.info("Screening Indian market (NSE)...")

        # Override markets to NSE
        results = self.screen_for_opportunities(
            markets=['NSE'],
            min_score=min_score,
            max_results=max_results
        )

        return results

    def screen_canadian_market(
        self,
        min_score: float = 65.0,
        max_results: int = 50
    ) -> pd.DataFrame:
        """Screen Canadian market (TSX) for opportunities.

        Args:
            min_score: Minimum overall score
            max_results: Maximum number of results

        Returns:
            DataFrame with Canadian market opportunities
        """
        logger.info("Screening Canadian market (TSX)...")

        # Override markets to TSX
        results = self.screen_for_opportunities(
            markets=['TSX'],
            min_score=min_score,
            max_results=max_results
        )

        return results

    def screen_us_market(
        self,
        min_score: float = 65.0,
        max_results: int = 50
    ) -> pd.DataFrame:
        """Screen US market (NASDAQ, NYSE) for opportunities.

        Args:
            min_score: Minimum overall score
            max_results: Maximum number of results

        Returns:
            DataFrame with US market opportunities
        """
        logger.info("Screening US market (NASDAQ, NYSE)...")

        # Override markets to US exchanges
        results = self.screen_for_opportunities(
            markets=['NASDAQ', 'NYSE'],
            min_score=min_score,
            max_results=max_results
        )

        return results


__all__ = ['StockScreener']
