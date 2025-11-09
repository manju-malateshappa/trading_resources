"""Data fetching module for stock market data."""

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Union
from alpha_vantage.fundamentaldata import FundamentalData
from alpha_vantage.timeseries import TimeSeries
import requests
import time

from ..utils.logger import logger
from ..utils.config_loader import config
from .company_database import company_db


class DataFetcher:
    """Fetch stock market data from various sources."""

    def __init__(self):
        """Initialize data fetcher with API keys."""
        api_keys = config.get_api_keys()
        self.alpha_vantage_key = api_keys.get('alpha_vantage')
        self.finnhub_key = api_keys.get('finnhub')
        self.news_api_key = api_keys.get('news_api')

        # Initialize API clients
        if self.alpha_vantage_key:
            self.fd = FundamentalData(key=self.alpha_vantage_key, output_format='pandas')
            self.ts = TimeSeries(key=self.alpha_vantage_key, output_format='pandas')

    def get_stock_data(
        self,
        symbol: str,
        period: str = "2y",
        interval: str = "1d"
    ) -> pd.DataFrame:
        """Fetch historical stock price data.

        Args:
            symbol: Stock ticker symbol (e.g., 'AAPL', 'SHOP.TO')
            period: Data period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)
            interval: Data interval (1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo)

        Returns:
            DataFrame with OHLCV data
        """
        try:
            logger.info(f"Fetching data for {symbol} (period={period}, interval={interval})")
            ticker = yf.Ticker(symbol)
            df = ticker.history(period=period, interval=interval)

            if df.empty:
                logger.warning(f"No data returned for {symbol}")
                return pd.DataFrame()

            logger.info(f"Successfully fetched {len(df)} rows for {symbol}")
            return df

        except Exception as e:
            logger.error(f"Error fetching data for {symbol}: {str(e)}")
            return pd.DataFrame()

    def get_fundamental_data(self, symbol: str) -> Dict:
        """Fetch fundamental data for a stock.

        Args:
            symbol: Stock ticker symbol

        Returns:
            Dictionary containing fundamental metrics
        """
        try:
            logger.info(f"Fetching fundamental data for {symbol}")
            ticker = yf.Ticker(symbol)
            info = ticker.info

            # Extract key fundamental metrics
            fundamentals = {
                'symbol': symbol,
                'name': info.get('longName', ''),
                'sector': info.get('sector', ''),
                'industry': info.get('industry', ''),
                'market_cap': info.get('marketCap', 0),
                'enterprise_value': info.get('enterpriseValue', 0),

                # Valuation metrics
                'pe_ratio': info.get('trailingPE', None),
                'forward_pe': info.get('forwardPE', None),
                'peg_ratio': info.get('pegRatio', None),
                'price_to_book': info.get('priceToBook', None),
                'price_to_sales': info.get('priceToSalesTrailing12Months', None),
                'ev_to_revenue': info.get('enterpriseToRevenue', None),
                'ev_to_ebitda': info.get('enterpriseToEbitda', None),

                # Profitability metrics
                'profit_margin': info.get('profitMargins', None),
                'operating_margin': info.get('operatingMargins', None),
                'gross_margin': info.get('grossMargins', None),
                'roe': info.get('returnOnEquity', None),
                'roa': info.get('returnOnAssets', None),

                # Growth metrics
                'revenue_growth': info.get('revenueGrowth', None),
                'earnings_growth': info.get('earningsGrowth', None),
                'revenue': info.get('totalRevenue', None),
                'earnings': info.get('netIncomeToCommon', None),

                # Financial health
                'current_ratio': info.get('currentRatio', None),
                'quick_ratio': info.get('quickRatio', None),
                'debt_to_equity': info.get('debtToEquity', None),
                'total_debt': info.get('totalDebt', 0),
                'total_cash': info.get('totalCash', 0),
                'free_cash_flow': info.get('freeCashflow', None),

                # Dividend metrics
                'dividend_yield': info.get('dividendYield', 0),
                'payout_ratio': info.get('payoutRatio', None),

                # Trading metrics
                'beta': info.get('beta', None),
                'avg_volume': info.get('averageVolume', 0),
                '52w_high': info.get('fiftyTwoWeekHigh', None),
                '52w_low': info.get('fiftyTwoWeekLow', None),
                'current_price': info.get('currentPrice', None),

                # Ownership
                'insider_ownership': info.get('heldPercentInsiders', 0),
                'institutional_ownership': info.get('heldPercentInstitutions', 0),

                # Target prices
                'target_high': info.get('targetHighPrice', None),
                'target_low': info.get('targetLowPrice', None),
                'target_mean': info.get('targetMeanPrice', None),
                'recommendation': info.get('recommendationKey', ''),
            }

            logger.info(f"Successfully fetched fundamental data for {symbol}")
            return fundamentals

        except Exception as e:
            logger.error(f"Error fetching fundamental data for {symbol}: {str(e)}")
            return {}

    def get_financial_statements(self, symbol: str) -> Dict[str, pd.DataFrame]:
        """Fetch financial statements.

        Args:
            symbol: Stock ticker symbol

        Returns:
            Dictionary containing income statement, balance sheet, and cash flow
        """
        try:
            logger.info(f"Fetching financial statements for {symbol}")
            ticker = yf.Ticker(symbol)

            statements = {
                'income_statement': ticker.financials,
                'balance_sheet': ticker.balance_sheet,
                'cash_flow': ticker.cashflow,
                'quarterly_income': ticker.quarterly_financials,
                'quarterly_balance': ticker.quarterly_balance_sheet,
                'quarterly_cashflow': ticker.quarterly_cashflow,
            }

            logger.info(f"Successfully fetched financial statements for {symbol}")
            return statements

        except Exception as e:
            logger.error(f"Error fetching financial statements for {symbol}: {str(e)}")
            return {}

    def get_earnings_history(self, symbol: str) -> pd.DataFrame:
        """Fetch earnings history.

        Args:
            symbol: Stock ticker symbol

        Returns:
            DataFrame with earnings data
        """
        try:
            logger.info(f"Fetching earnings history for {symbol}")
            ticker = yf.Ticker(symbol)
            earnings = ticker.earnings

            return earnings if earnings is not None else pd.DataFrame()

        except Exception as e:
            logger.error(f"Error fetching earnings for {symbol}: {str(e)}")
            return pd.DataFrame()

    def get_news(self, symbol: str, limit: int = 10) -> List[Dict]:
        """Fetch recent news for a stock.

        Args:
            symbol: Stock ticker symbol
            limit: Number of news articles to fetch

        Returns:
            List of news articles
        """
        try:
            logger.info(f"Fetching news for {symbol}")

            if self.finnhub_key:
                # Use Finnhub API
                url = f"https://finnhub.io/api/v1/company-news"
                params = {
                    'symbol': symbol,
                    'from': (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'),
                    'to': datetime.now().strftime('%Y-%m-%d'),
                    'token': self.finnhub_key
                }
                response = requests.get(url, params=params)

                if response.status_code == 200:
                    news = response.json()[:limit]
                    return news
            else:
                # Fallback to yfinance
                ticker = yf.Ticker(symbol)
                news = ticker.news[:limit] if hasattr(ticker, 'news') else []
                return news

        except Exception as e:
            logger.error(f"Error fetching news for {symbol}: {str(e)}")
            return []

    def get_market_cap_range_stocks(
        self,
        min_cap: float = 100_000_000,  # $100M
        max_cap: float = 10_000_000_000,  # $10B
        market: str = "TSX"
    ) -> List[str]:
        """Get list of stocks within a market cap range.

        Args:
            min_cap: Minimum market cap
            max_cap: Maximum market cap
            market: Market (TSX, TSXV, NASDAQ, NYSE, NSE, BSE)

        Returns:
            List of ticker symbols
        """
        logger.info(f"Fetching {market} stocks with market cap ${min_cap:,.0f} - ${max_cap:,.0f}")

        # Get companies from database based on market
        if market in ["NASDAQ", "NYSE"]:
            market_filter = "USA"
        elif market in ["TSX", "TSXV"]:
            market_filter = "CANADA"
        elif market in ["NSE", "BSE"]:
            market_filter = "INDIA"
        else:
            market_filter = None

        # Get all symbols from company database
        tickers = company_db.get_all_symbols(market=market_filter)

        logger.info(f"Found {len(tickers)} symbols from company database for {market}")

        return tickers

    def get_ai_companies(self, market: str = None) -> List[str]:
        """Get AI company symbols.

        Args:
            market: Market filter ('USA', 'CANADA', 'INDIA', or None for all)

        Returns:
            List of AI company symbols
        """
        logger.info(f"Fetching AI companies for market: {market or 'ALL'}")

        ai_companies = company_db.get_all_ai_companies(market=market)
        symbols = [c['symbol'] for c in ai_companies]

        logger.info(f"Found {len(symbols)} AI companies")

        return symbols

    def get_sector_companies(self, sector: str, market: str = None) -> List[str]:
        """Get companies by sector.

        Args:
            sector: Sector name (e.g., 'Fintech', 'Cloud Computing', 'EV & Clean Energy')
            market: Market filter ('USA', 'CANADA', 'INDIA', or None for all)

        Returns:
            List of company symbols
        """
        logger.info(f"Fetching {sector} companies for market: {market or 'ALL'}")

        companies = company_db.get_companies_by_sector(sector, market=market)
        symbols = [c['symbol'] for c in companies]

        logger.info(f"Found {len(symbols)} companies in {sector}")

        return symbols

    def normalize_indian_symbol(self, symbol: str, exchange: str = "NSE") -> str:
        """Normalize Indian stock symbol for yfinance.

        Args:
            symbol: Stock symbol
            exchange: Exchange ('NSE' or 'BSE')

        Returns:
            Normalized symbol for yfinance
        """
        # Remove any existing suffixes
        base_symbol = symbol.replace('.NS', '').replace('.BO', '').replace('.BSE', '')

        # Add appropriate suffix
        if exchange.upper() == "BSE":
            return f"{base_symbol}.BO"
        else:  # Default to NSE
            return f"{base_symbol}.NS"

    def batch_fetch_fundamentals(self, symbols: List[str]) -> pd.DataFrame:
        """Fetch fundamental data for multiple stocks.

        Args:
            symbols: List of ticker symbols

        Returns:
            DataFrame with fundamental data for all symbols
        """
        logger.info(f"Batch fetching fundamentals for {len(symbols)} symbols")

        data_list = []
        for symbol in symbols:
            try:
                data = self.get_fundamental_data(symbol)
                if data:
                    data_list.append(data)
                time.sleep(0.5)  # Rate limiting
            except Exception as e:
                logger.error(f"Error in batch fetch for {symbol}: {str(e)}")
                continue

        df = pd.DataFrame(data_list)
        logger.info(f"Successfully fetched data for {len(df)} symbols")
        return df


__all__ = ['DataFetcher']
