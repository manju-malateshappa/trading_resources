# Quick Start Guide 🚀

Get up and running with the Investment Agent in 5 minutes!

## Step 1: Install Dependencies (2 minutes)

```bash
# Install Python packages
pip install -r requirements.txt
```

## Step 2: Configure (Optional - 1 minute)

```bash
# Copy environment template
cp .env.example .env

# Edit .env and add API keys (optional but recommended)
# nano .env
```

**Note**: The agent works without API keys using free data from Yahoo Finance!

## Step 3: Run Your First Scan (2 minutes)

### Option A: Using CLI

**Scan for opportunities:**
```bash
python main.py scan --markets TSX NASDAQ
```

**Get recommendations:**
```bash
python main.py recommend --focus growth --min-score 70
```

**Analyze a specific stock:**
```bash
python main.py analyze SHOP.TO
```

### Option B: Using Python

```python
from investment_agent.agent import InvestmentAgent

# Initialize
agent = InvestmentAgent()

# Scan market
opportunities = agent.scan_market(markets=['TSX', 'NASDAQ'])

# Show top 5
print(opportunities.head(5)[['symbol', 'name', 'overall_score', 'expected_return_2y']])
```

## Step 4: Try the Examples

```bash
python examples/basic_usage.py
```

## What's Next?

1. **Review the Configuration**: Edit `investment_agent/config/settings.yaml` to customize entry/exit criteria
2. **Set Up Daily Scans**: Run `python main.py daily` every morning
3. **Paper Trade**: Test the system before using real money
4. **Read Full Docs**: Check out `README.md` for comprehensive documentation

## Common Commands

```bash
# Scan market
python main.py scan

# Get recommendations
python main.py recommend

# Analyze a stock
python main.py analyze AAPL

# Evaluate buying
python main.py buy SHOP.TO

# Daily routine
python main.py daily

# View portfolio
python main.py portfolio
```

## Need Help?

- Check `README.md` for full documentation
- Review `examples/basic_usage.py` for code examples
- Verify `settings.yaml` for configuration options

**Happy investing! 📈**
