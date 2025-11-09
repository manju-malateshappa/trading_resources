"""Main Investment Agent orchestrator."""

import pandas as pd
from typing import Dict, List, Optional
from datetime import datetime
import time

from .data.data_fetcher import DataFetcher
from .analysis.fundamental_analyzer import FundamentalAnalyzer
from .analysis.technical_analyzer import TechnicalAnalyzer
from .strategy.stock_screener import StockScreener
from .portfolio.portfolio_manager import PortfolioManager, Portfolio
from .risk.risk_manager import RiskManager
from .utils.logger import logger
from .utils.config_loader import config


class InvestmentAgent:
    """Main investment agent that orchestrates all components."""

    def __init__(self, portfolio_name: str = "Main Portfolio"):
        """Initialize investment agent.

        Args:
            portfolio_name: Name of portfolio to manage
        """
        logger.info("=" * 60)
        logger.info("INITIALIZING INVESTMENT AGENT")
        logger.info("=" * 60)

        # Initialize components
        self.data_fetcher = DataFetcher()
        self.fundamental_analyzer = FundamentalAnalyzer()
        self.technical_analyzer = TechnicalAnalyzer()
        self.stock_screener = StockScreener()
        self.portfolio_manager = PortfolioManager()
        self.risk_manager = RiskManager()

        # Load or create portfolio
        self.portfolio = self.portfolio_manager.get_portfolio(portfolio_name)
        if self.portfolio is None:
            initial_capital = float(config.get_env('INITIAL_CAPITAL', 100000))
            self.portfolio = self.portfolio_manager.create_portfolio(
                portfolio_name,
                initial_capital
            )

        self.portfolio_name = portfolio_name

        logger.info(f"Portfolio: {portfolio_name}")
        logger.info(f"Cash: ${self.portfolio.cash:,.2f}")
        logger.info(f"Positions: {len(self.portfolio.positions)}")
        logger.info("=" * 60)

    def scan_market(self, markets: List[str] = None) -> pd.DataFrame:
        """Scan market for investment opportunities.

        Args:
            markets: List of markets to scan (default: from config)

        Returns:
            DataFrame with opportunities
        """
        logger.info("Starting market scan...")

        opportunities = self.stock_screener.screen_for_opportunities(
            markets=markets,
            min_score=65.0,
            max_results=50
        )

        if not opportunities.empty:
            logger.info(f"\nFound {len(opportunities)} opportunities:")
            logger.info("\nTop 10 by overall score:")
            top_10 = opportunities.head(10)[
                ['symbol', 'name', 'overall_score', 'recommendation',
                 'expected_return_2y', 'risk_level']
            ]
            logger.info(f"\n{top_10.to_string()}")

        return opportunities

    def analyze_stock(self, symbol: str) -> Dict:
        """Perform comprehensive analysis of a stock.

        Args:
            symbol: Stock ticker symbol

        Returns:
            Complete analysis results
        """
        logger.info(f"\n{'=' * 60}")
        logger.info(f"ANALYZING: {symbol}")
        logger.info(f"{'=' * 60}")

        # Fetch fundamental data
        fundamentals = self.data_fetcher.get_fundamental_data(symbol)
        if not fundamentals:
            logger.error(f"Could not fetch data for {symbol}")
            return {}

        # Fundamental analysis
        fund_analysis = self.fundamental_analyzer.analyze_stock(fundamentals)

        # Fetch price data
        price_data = self.data_fetcher.get_stock_data(symbol, period="2y", interval="1d")

        # Technical analysis
        tech_analysis = self.technical_analyzer.analyze_stock(price_data, symbol)

        # Combine results
        analysis = {
            'symbol': symbol,
            'name': fundamentals.get('name'),
            'sector': fundamentals.get('sector'),
            'current_price': fundamentals.get('current_price'),
            'fundamentals': fund_analysis,
            'technicals': tech_analysis,
            'timestamp': datetime.now().isoformat(),
        }

        # Display summary
        self._display_analysis_summary(analysis)

        return analysis

    def get_recommendations(
        self,
        min_score: float = 70.0,
        focus: str = 'growth'
    ) -> pd.DataFrame:
        """Get investment recommendations.

        Args:
            min_score: Minimum overall score
            focus: Focus type ('growth', 'value', 'breakout')

        Returns:
            DataFrame with recommendations
        """
        logger.info(f"\nGenerating {focus} recommendations (min score: {min_score})...")

        if focus == 'growth':
            recommendations = self.stock_screener.screen_for_opportunities(
                min_score=min_score,
                max_results=20
            )
        elif focus == 'value':
            recommendations = self.stock_screener.find_value_opportunities()
        elif focus == 'breakout':
            recommendations = self.stock_screener.find_breakout_candidates()
        else:
            recommendations = self.stock_screener.screen_for_opportunities(
                min_score=min_score
            )

        if not recommendations.empty:
            logger.info(f"\nTop {focus} recommendations:")
            display_cols = [
                'symbol', 'name', 'overall_score', 'recommendation',
                'expected_return_2y', 'risk_level', 'current_price'
            ]
            logger.info(f"\n{recommendations[display_cols].head(10).to_string()}")

        return recommendations

    def evaluate_buy(
        self,
        symbol: str,
        shares: int = None
    ) -> Dict:
        """Evaluate buying a stock.

        Args:
            symbol: Stock ticker symbol
            shares: Number of shares (optional, will calculate if not provided)

        Returns:
            Evaluation results with recommendation
        """
        logger.info(f"\nEvaluating BUY for {symbol}...")

        # Analyze stock
        analysis = self.analyze_stock(symbol)
        if not analysis:
            return {'action': 'SKIP', 'reason': 'Analysis failed'}

        fundamentals = self.data_fetcher.get_fundamental_data(symbol)
        current_price = fundamentals.get('current_price', 0)

        # Calculate position size if not provided
        if shares is None:
            shares, position_value = self.risk_manager.calculate_position_size(
                self.portfolio,
                symbol,
                current_price,
                conviction=analysis['fundamentals'].get('overall_score', 50) / 100
            )

        # Check limits
        current_prices = {symbol: current_price}
        sector = fundamentals.get('sector', 'Unknown')

        within_limits = self.risk_manager.check_position_limits(
            self.portfolio,
            symbol,
            shares,
            current_price,
            current_prices
        )

        if not within_limits:
            return {
                'action': 'SKIP',
                'reason': 'Exceeds position or cash limits',
                'symbol': symbol,
                'current_price': current_price,
            }

        # Get recommendation
        recommendation = analysis['fundamentals'].get('buy_signal', 'hold')
        overall_score = analysis['fundamentals'].get('overall_score', 0)

        # Calculate entry/exit levels
        stop_loss = self.risk_manager.calculate_stop_loss(current_price)
        take_profit_levels = self.risk_manager.calculate_take_profit_levels(current_price)

        evaluation = {
            'action': 'BUY' if recommendation in ['buy', 'strong_buy'] else 'HOLD',
            'symbol': symbol,
            'shares': shares,
            'current_price': current_price,
            'total_cost': shares * current_price,
            'recommendation': recommendation,
            'overall_score': overall_score,
            'stop_loss': stop_loss,
            'take_profit_levels': take_profit_levels,
            'risk_level': analysis['fundamentals'].get('risk_level'),
            'expected_return_2y': analysis['fundamentals'].get('growth_potential', {}).get('expected_2y', 0),
        }

        logger.info(f"\nEvaluation: {evaluation['action']}")
        logger.info(f"Shares: {shares} @ ${current_price:.2f} = ${shares * current_price:,.2f}")
        logger.info(f"Stop Loss: ${stop_loss:.2f} ({((stop_loss - current_price) / current_price):.1%})")
        logger.info(f"Overall Score: {overall_score:.1f}")

        return evaluation

    def evaluate_sell(self, symbol: str) -> Dict:
        """Evaluate selling a stock.

        Args:
            symbol: Stock ticker symbol

        Returns:
            Evaluation results with recommendation
        """
        logger.info(f"\nEvaluating SELL for {symbol}...")

        if symbol not in self.portfolio.positions:
            return {'action': 'SKIP', 'reason': f'No position in {symbol}'}

        position = self.portfolio.positions[symbol]

        # Get current data
        fundamentals = self.data_fetcher.get_fundamental_data(symbol)
        current_price = fundamentals.get('current_price', 0)

        # Calculate return
        position_return = position.get_return(current_price)
        profit_loss = position.get_profit_loss(current_price)

        # Check fundamental deterioration
        exit_signals = self.fundamental_analyzer.check_exit_signals(fundamentals)

        # Check technical signals
        price_data = self.data_fetcher.get_stock_data(symbol, period="1y", interval="1d")
        tech_analysis = self.technical_analyzer.analyze_stock(price_data, symbol)
        tech_signal = tech_analysis.get('overall_signal', 'hold')

        # Check stop-loss
        stop_loss = self.risk_manager.calculate_stop_loss(position.entry_price)
        stop_triggered = current_price <= stop_loss

        # Check trailing stop
        trailing_stop = self.risk_manager.calculate_trailing_stop(
            position.entry_price,
            current_price
        )
        trailing_stop_triggered = trailing_stop and current_price <= trailing_stop

        # Determine action
        should_sell = False
        reason = []

        if stop_triggered:
            should_sell = True
            reason.append(f"Stop-loss triggered (${stop_loss:.2f})")

        if trailing_stop_triggered:
            should_sell = True
            reason.append(f"Trailing stop triggered (${trailing_stop:.2f})")

        if exit_signals:
            should_sell = True
            reason.extend(exit_signals)

        if tech_signal in ['sell', 'strong_sell']:
            should_sell = True
            reason.append(f"Technical signal: {tech_signal}")

        # Check take-profit levels
        take_profit_levels = self.risk_manager.calculate_take_profit_levels(position.entry_price)
        for level_name, level_data in take_profit_levels.items():
            if current_price >= level_data['price']:
                reason.append(f"Take-profit level reached: {level_name}")

        evaluation = {
            'action': 'SELL' if should_sell else 'HOLD',
            'symbol': symbol,
            'shares': position.shares,
            'entry_price': position.entry_price,
            'current_price': current_price,
            'return': position_return,
            'profit_loss': profit_loss,
            'reasons': reason,
            'stop_loss': stop_loss,
            'trailing_stop': trailing_stop,
            'exit_signals': exit_signals,
        }

        logger.info(f"\nEvaluation: {evaluation['action']}")
        logger.info(f"Return: {position_return:.1%}")
        logger.info(f"P/L: ${profit_loss:,.2f}")
        if reason:
            logger.info(f"Reasons: {', '.join(reason)}")

        return evaluation

    def daily_routine(self) -> Dict:
        """Run daily routine: scan market and monitor positions.

        Returns:
            Dictionary with results
        """
        logger.info("\n" + "=" * 60)
        logger.info(f"DAILY ROUTINE - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info("=" * 60)

        results = {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'opportunities': None,
            'position_alerts': [],
            'portfolio_summary': {},
        }

        # 1. Scan for new opportunities
        logger.info("\n1. Scanning market for opportunities...")
        opportunities = self.scan_market()
        results['opportunities'] = opportunities

        # 2. Monitor existing positions
        logger.info("\n2. Monitoring existing positions...")
        for symbol in list(self.portfolio.positions.keys()):
            evaluation = self.evaluate_sell(symbol)
            if evaluation['action'] == 'SELL':
                results['position_alerts'].append(evaluation)

        # 3. Portfolio summary
        logger.info("\n3. Portfolio summary...")
        current_prices = {}
        for symbol in self.portfolio.positions.keys():
            fund_data = self.data_fetcher.get_fundamental_data(symbol)
            current_prices[symbol] = fund_data.get('current_price', 0)

        total_value = self.portfolio.get_total_value(current_prices)
        total_return = self.portfolio.get_return(current_prices)

        results['portfolio_summary'] = {
            'total_value': total_value,
            'cash': self.portfolio.cash,
            'return': total_return,
            'num_positions': len(self.portfolio.positions),
        }

        logger.info(f"\nPortfolio Value: ${total_value:,.2f}")
        logger.info(f"Return: {total_return:.2%}")
        logger.info(f"Positions: {len(self.portfolio.positions)}")
        logger.info(f"Cash: ${self.portfolio.cash:,.2f}")

        return results

    def _display_analysis_summary(self, analysis: Dict) -> None:
        """Display analysis summary.

        Args:
            analysis: Analysis results
        """
        logger.info(f"\nCompany: {analysis.get('name')}")
        logger.info(f"Sector: {analysis.get('sector')}")
        logger.info(f"Current Price: ${analysis.get('current_price', 0):.2f}")

        fund = analysis.get('fundamentals', {})
        logger.info(f"\nFundamental Score: {fund.get('overall_score', 0):.1f}/100")
        logger.info(f"Signal: {fund.get('buy_signal', 'unknown').upper()}")
        logger.info(f"Growth Score: {fund.get('growth_score', 0):.1f}/100")
        logger.info(f"Risk Level: {fund.get('risk_level', 'unknown')}")

        tech = analysis.get('technicals', {})
        logger.info(f"\nTechnical Score: {tech.get('signal_strength', 0):.1f}/100")
        logger.info(f"Signal: {tech.get('overall_signal', 'unknown').upper()}")
        logger.info(f"Trend: {tech.get('trend', 'unknown')}")
        logger.info(f"RSI: {tech.get('rsi', 0):.1f}")

        potential = fund.get('growth_potential', {})
        logger.info(f"\nExpected 2Y Return: {potential.get('expected_2y', 0):.1%}")
        logger.info(f"Optimistic 2Y Return: {potential.get('optimistic_2y', 0):.1%}")


__all__ = ['InvestmentAgent']
