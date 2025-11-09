# Investment Agent 🤖📈

An AI-powered investment analysis and portfolio management system specializing in identifying high-growth small/mid-cap stocks with potential for 100-200% returns within 1-2 years.

## 🎯 Overview

The Investment Agent is a comprehensive automated system that combines:
- **Fundamental Analysis**: Deep dive into company financials, growth metrics, and valuation
- **Technical Analysis**: Chart patterns, momentum indicators, and trend analysis
- **Risk Management**: Position sizing, stop-loss, and portfolio diversification
- **Portfolio Management**: Track positions, calculate returns, and optimize allocation
- **Tax Optimization**: Canadian tax rules (TFSA, RRSP, capital gains)
- **Automated Screening**: Daily/weekly scans for emerging opportunities

## ✨ Key Features

### Investment Strategy
- **Buy-and-Hold with Strategic Exits**: Long-term investment with defined exit criteria
- **Growth-Focused**: Target 100-200% returns over 1-2 years
- **Small/Mid-Cap Focus**: $100M - $10B market cap range
- **Multi-Factor Analysis**: Combines fundamental, technical, and sentiment analysis

### Analysis Capabilities
1. **Fundamental Analysis**
   - Revenue and earnings growth analysis
   - Profitability metrics (margins, ROE, ROA)
   - Financial health (debt levels, liquidity ratios)
   - Valuation metrics (P/E, PEG, P/B, P/S)
   - Quality scoring (institutional ownership, analyst ratings)

2. **Technical Analysis**
   - Trend identification (uptrend, downtrend, sideways)
   - Momentum indicators (RSI, MACD, Stochastic)
   - Moving averages (SMA, EMA)
   - Volume analysis and breakout detection
   - Support/resistance level identification

3. **Risk Management**
   - Automated position sizing using Kelly Criterion
   - Stop-loss and trailing stop calculations
   - Sector concentration limits
   - Portfolio volatility monitoring
   - Maximum drawdown tracking

4. **Tax Optimization**
   - TFSA prioritization for high-growth stocks
   - Capital gains tax planning
   - Tax-loss harvesting
   - Superficial loss rule compliance (30-day rule)

## 🚀 Quick Start

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd trading_resources
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env and add your API keys (optional but recommended)
```

4. **Configure settings** (optional)
Edit `investment_agent/config/settings.yaml` to customize:
- Entry/exit criteria
- Risk parameters
- Screening filters
- Portfolio limits

### Basic Usage

#### Command Line Interface

**Scan market for opportunities:**
```bash
python main.py scan --markets TSX NASDAQ
```

**Analyze a specific stock:**
```bash
python main.py analyze SHOP.TO
```

**Get investment recommendations:**
```bash
python main.py recommend --focus growth --min-score 70
```

**Evaluate buying a stock:**
```bash
python main.py buy LSPD.TO
```

**Evaluate selling a position:**
```bash
python main.py sell SHOP.TO
```

**Run daily routine:**
```bash
python main.py daily
```

**View portfolio:**
```bash
python main.py portfolio
```

#### Python API

```python
from investment_agent.agent import InvestmentAgent

# Initialize agent
agent = InvestmentAgent(portfolio_name="My Portfolio")

# Scan market for opportunities
opportunities = agent.scan_market(markets=['TSX', 'NASDAQ'])

# Analyze a specific stock
analysis = agent.analyze_stock('SHOP.TO')

# Get recommendations
recommendations = agent.get_recommendations(
    min_score=70.0,
    focus='growth'  # 'growth', 'value', or 'breakout'
)

# Evaluate a buy
evaluation = agent.evaluate_buy('LSPD.TO')

# Run daily routine
results = agent.daily_routine()
```

## 📊 Investment Criteria

### Entry Criteria (Configurable)
- **Revenue Growth**: Minimum 15% YoY
- **P/E Ratio**: Maximum 30 (flexible for high-growth)
- **Profit Margin**: Minimum 5%
- **Debt-to-Equity**: Maximum 2.0
- **Current Ratio**: Minimum 1.2
- **Market Cap**: $100M - $10B
- **Average Volume**: Minimum 50,000 shares/day

### Exit Criteria
**Take-Profit Levels:**
- 25% gain: Sell 20% of position
- 50% gain: Sell 25% of position
- 100% gain: Sell 30% of position
- 200% gain: Sell remaining position

**Stop-Loss:**
- 15% fixed stop-loss
- 10% trailing stop after 20% gain

**Fundamental Deterioration:**
- 2+ quarters of revenue decline
- 30% margin compression
- 50% debt increase
- Analyst downgrades to sell

## 🎓 Examples

See `examples/basic_usage.py` for comprehensive examples:

1. **Scan Market**: Find high-growth opportunities
2. **Analyze Stock**: Deep dive into a specific stock
3. **Evaluate Buy**: Determine if you should buy
4. **Get Recommendations**: Various recommendation types
5. **Daily Routine**: Automated daily workflow
6. **Portfolio Simulation**: Build a sample portfolio

Run examples:
```bash
python examples/basic_usage.py
```

## 📁 Project Structure

```
trading_resources/
├── investment_agent/
│   ├── agent.py                 # Main agent orchestrator
│   ├── data/
│   │   └── data_fetcher.py      # Stock data fetching
│   ├── analysis/
│   │   ├── fundamental_analyzer.py  # Fundamental analysis
│   │   └── technical_analyzer.py    # Technical analysis
│   ├── strategy/
│   │   └── stock_screener.py    # Stock screening
│   ├── portfolio/
│   │   └── portfolio_manager.py # Portfolio management
│   ├── risk/
│   │   └── risk_manager.py      # Risk management
│   ├── config/
│   │   └── settings.yaml        # Configuration
│   └── utils/
│       ├── logger.py            # Logging
│       └── config_loader.py     # Config loader
├── main.py                       # CLI interface
├── examples/
│   └── basic_usage.py           # Usage examples
├── requirements.txt              # Dependencies
├── .env.example                  # Environment template
└── README.md                     # This file
```

## 🔑 API Keys (Optional but Recommended)

The agent works with free data sources (yfinance) but enhanced features require API keys:

1. **Alpha Vantage** (Free): Enhanced fundamental data
   - Sign up: https://www.alphavantage.co/support/#api-key

2. **Finnhub** (Free): Real-time news and additional data
   - Sign up: https://finnhub.io/register

3. **News API** (Free): News sentiment analysis
   - Sign up: https://newsapi.org/register

4. **FRED** (Free): Economic data
   - Sign up: https://fred.stlouisfed.org/docs/api/api_key.html

Add keys to your `.env` file:
```env
ALPHA_VANTAGE_API_KEY=your_key_here
FINNHUB_API_KEY=your_key_here
NEWS_API_KEY=your_key_here
FRED_API_KEY=your_key_here
```

## ⚙️ Configuration

Edit `investment_agent/config/settings.yaml` to customize:

### Strategy Parameters
```yaml
strategy:
  entry:
    min_revenue_growth: 0.15      # 15% minimum
    max_pe_ratio: 30
    min_profit_margin: 0.05
  exit:
    take_profit_levels: [0.25, 0.50, 1.00, 2.00]
    stop_loss: 0.15
    trailing_stop: 0.10
```

### Portfolio Limits
```yaml
portfolio:
  max_positions: 20
  max_position_size: 0.15         # 15% max per stock
  max_sector_allocation: 0.30     # 30% max per sector
  cash_reserve: 0.10              # Keep 10% cash
```

### Risk Management
```yaml
risk:
  max_portfolio_volatility: 0.25
  max_drawdown: 0.20
  position_sizing:
    method: "kelly_criterion"
    kelly_fraction: 0.25
```

## 🤖 Automated Workflows

### Daily Routine
```bash
# Run every day at 9:00 AM (after market open)
python main.py daily
```

This will:
1. Scan market for new opportunities
2. Monitor existing positions for exit signals
3. Generate portfolio summary and alerts

### Weekly Deep Scan
```bash
# Run every Monday
python main.py scan --markets TSX TSXV NASDAQ NYSE
python main.py recommend --focus growth --min-score 65
```

### Setup Cron Job (Linux/Mac)
```bash
# Edit crontab
crontab -e

# Add daily routine at 9:00 AM
0 9 * * 1-5 cd /path/to/trading_resources && python main.py daily >> logs/daily.log 2>&1

# Add weekly scan on Monday at 10:00 AM
0 10 * * 1 cd /path/to/trading_resources && python main.py scan >> logs/weekly.log 2>&1
```

## 📈 Performance Metrics

The agent tracks comprehensive performance metrics:
- **Total Return**: Overall portfolio return %
- **Annualized Return**: Return annualized
- **Sharpe Ratio**: Risk-adjusted return
- **Sortino Ratio**: Downside risk-adjusted return
- **Maximum Drawdown**: Largest peak-to-trough decline
- **Win Rate**: Percentage of profitable trades
- **Profit Factor**: Gross profit / gross loss
- **Average Gain/Loss**: Average per winning/losing trade

## 🛡️ Risk Disclaimer

**IMPORTANT**: This software is for educational and research purposes only.

- **Not Financial Advice**: This is NOT financial advice. Always do your own research.
- **No Guarantees**: Past performance doesn't guarantee future results
- **High Risk**: Small/mid-cap stocks are volatile and risky
- **Paper Trading**: Test with paper trading before using real money
- **Consult Professionals**: Consult with licensed financial advisors
- **Tax Implications**: Understand tax implications of trading
- **Know Your Limits**: Only invest what you can afford to lose

## 🇨🇦 Canadian Tax Considerations

The agent includes Canadian tax optimization:

### TFSA (Tax-Free Savings Account)
- **Best for**: High-growth stocks (100%+ gains)
- **Tax on gains**: 0%
- **Contribution limit**: $88,000 (2024 cumulative)

### RRSP (Registered Retirement Savings Plan)
- **Best for**: Dividend-paying stocks
- **Tax benefit**: Deduction on contribution
- **Tax on withdrawal**: Marginal tax rate

### Taxable Account
- **Capital gains**: 50% inclusion rate
- **Tax-loss harvesting**: Offset gains with losses
- **Superficial loss rule**: Wait 30 days before repurchasing

## 🔄 Updates & Maintenance

### Update Stock Data
Stock data is fetched in real-time. For the best results:
- Run during market hours for real-time prices
- API rate limits apply (respect them)

### Update Configuration
After changing `settings.yaml`, restart the agent.

## 🐛 Troubleshooting

### Common Issues

**"No data returned for symbol"**
- Check if symbol is correct (use .TO for TSX stocks)
- Verify internet connection
- Check if market is open

**"Exceeds position limits"**
- Increase `max_position_size` in config
- Check available cash in portfolio

**"Rate limit exceeded"**
- Wait a few minutes between requests
- Consider using API keys for higher limits

**"Module not found"**
- Install all requirements: `pip install -r requirements.txt`
- Verify Python version (3.8+)

## 🤝 Contributing

Contributions are welcome! Areas for improvement:
- Additional data sources and APIs
- More sophisticated ML models
- Enhanced backtesting capabilities
- Additional market support (international)
- Mobile/web interface

## 📝 License

This project is for educational purposes. Use at your own risk.

## 📧 Support

For questions, issues, or suggestions:
- Open an issue on GitHub
- Check examples in `examples/` directory
- Review configuration in `investment_agent/config/settings.yaml`

---

## 🎯 Quick Reference

### Best Practices

1. **Start with paper trading** to test the system
2. **Run daily routine** every morning
3. **Review recommendations** before buying
4. **Set stop-losses** on all positions
5. **Diversify** across sectors
6. **Keep cash reserves** (10-20%)
7. **Track performance** regularly
8. **Rebalance quarterly**
9. **Take profits** at target levels
10. **Stay disciplined** with the strategy

### Recommended Workflow

**Week 1: Setup**
- Install and configure
- Run market scans
- Study top opportunities
- Paper trade

**Week 2-4: Testing**
- Continue paper trading
- Track recommendations
- Monitor performance
- Refine criteria

**Month 2+: Live Trading**
- Start with small positions
- Follow entry/exit rules
- Monitor daily
- Review monthly

---

**Happy Investing! 🚀📈**

*Remember: The best investment is in your own knowledge. Always keep learning!*
