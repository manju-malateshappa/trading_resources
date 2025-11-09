# Investment Agent - Complete Command Guide 📖

Quick reference for all available commands in the Investment Agent.

## 🚀 Getting Started

```bash
# Show help
python main.py help

# Quick start guide
python main.py quick

# Version info
python main.py version
```

## 📊 Stock Analysis Commands

### Analyze Stock
```bash
# Deep dive analysis (fundamental + technical)
python main.py analyze NVDA
python main.py analyze TCS.NS
python main.py analyze SHOP.TO

# Get detailed help
python main.py help analyze
```

### Quick Info
```bash
# Quick snapshot: price, market cap, P/E, growth, margin
python main.py info NVDA
python main.py info INFY.NS
python main.py info LSPD.TO
```

### Score Breakdown
```bash
# Show detailed score breakdown with ratings
python main.py score PLTR
python main.py score PERSISTENT.NS

# Shows:
# - Overall Score
# - Growth Score
# - Valuation Score
# - Profitability Score
# - Financial Health Score
# - Quality Score
# - Buy Signal & Risk Level
```

### Evaluate Buy/Sell
```bash
# Evaluate buying
python main.py buy CRWD
python main.py buy TCS.NS --shares 100

# Evaluate selling
python main.py sell SHOP.TO
python main.py sell INFY.NS
```

## 🌍 Market Scanning Commands

### General Scan
```bash
# Scan default markets
python main.py scan

# Scan specific markets
python main.py scan --markets TSX NASDAQ
python main.py scan --markets NSE BSE
```

### AI Companies
```bash
# Scan ALL AI companies (USA + Canada + India)
python main.py ai

# Scan AI by market
python main.py ai --market USA        # 30+ US AI companies
python main.py ai --market CANADA     # 12+ Canadian AI companies
python main.py ai --market INDIA      # 16+ Indian AI companies

# With minimum score filter
python main.py ai --market USA --min-score 75

# Get help
python main.py help ai
```

### Sector Scanning
```bash
# Scan specific sector (all markets)
python main.py sector Fintech
python main.py sector "Cloud Computing"
python main.py sector "IT Services"
python main.py sector "EV & Clean Energy"

# Scan sector in specific market
python main.py sector Fintech --market USA
python main.py sector "IT Services" --market INDIA
python main.py sector "Cloud Computing" --market USA

# With minimum score
python main.py sector Fintech --min-score 70

# Get help
python main.py help sector
```

**Available Sectors:**
- Fintech
- Cloud Computing
- Cybersecurity
- IT Services
- EV & Clean Energy
- Healthcare
- E-commerce
- Biotech
- Gaming

### Market-Specific Scans
```bash
# Scan Indian market (NSE/BSE)
python main.py india
python main.py india --min-score 70

# Scan Canadian market (TSX/TSXV)
python main.py canada
python main.py canada --min-score 65

# Scan US market (NASDAQ/NYSE)
python main.py us
python main.py us --min-score 75
```

## 🔍 Screening & Recommendations

### Get Recommendations
```bash
# General recommendations
python main.py recommend

# Focus-specific recommendations
python main.py recommend --focus growth      # High-growth stocks
python main.py recommend --focus value       # Undervalued stocks
python main.py recommend --focus breakout    # Technical breakouts

# With score filter
python main.py recommend --focus growth --min-score 75

# Get help
python main.py help recommend
```

### Top Stocks
```bash
# Top 10 opportunities (default)
python main.py top

# Top N stocks
python main.py top 5
python main.py top 20
python main.py top 30

# Top N in specific market
python main.py top 10 --market USA
python main.py top 15 --market CANADA
python main.py top 20 --market INDIA
```

## ⭐ Favorites Management

### Add to Favorites
```bash
# Add to general category
python main.py fav add NVDA

# Add to specific category
python main.py fav add NVDA ai
python main.py fav add TCS.NS india
python main.py fav add SHOP.TO canada
python main.py fav add CRWD tech
python main.py fav add PLTR ai

# Multiple examples
python main.py fav add INFY.NS india
python main.py fav add LSPD.TO tech
python main.py fav add PERSISTENT.NS ai
```

### Remove from Favorites
```bash
python main.py fav remove NVDA
python main.py fav remove SHOP.TO
```

### View Favorites
```bash
# Show all favorites
python main.py fav show

# Show specific category
python main.py fav show ai
python main.py fav show usa
python main.py fav show canada
python main.py fav show india
python main.py fav show tech
python main.py fav show healthcare
python main.py fav show fintech
python main.py fav show watchlist

# Just use 'fav' to show all
python main.py fav
```

### Manage Categories
```bash
# List all categories with counts
python main.py fav categories
```

**Default Categories:**
- general
- usa
- canada
- india
- ai
- tech
- healthcare
- fintech
- watchlist

### Scan Favorites
```bash
# Scan all favorites for buy signals
python main.py fav scan

# This will:
# 1. Analyze each favorite stock
# 2. Check for buy signals
# 3. Show which favorites are ready to buy
# 4. Display scores and recommendations
```

### Export Favorites
```bash
# Export to JSON
python main.py fav export my_favorites.json

# Export to CSV
python main.py fav export my_favorites.csv
```

## 💼 Portfolio Management

### View Portfolio
```bash
# Complete portfolio overview
python main.py portfolio

# Shows:
# - All positions
# - Cash balance
# - Total value
# - Entry prices
# - Allocation
```

### Daily Routine
```bash
# Run daily routine
python main.py daily

# This will:
# 1. Scan markets for new opportunities
# 2. Monitor existing positions for exit signals
# 3. Generate portfolio summary
# 4. Show position alerts
```

## 🔧 Utility Commands

### Help
```bash
# Show all commands
python main.py help

# Help on specific command
python main.py help analyze
python main.py help ai
python main.py help sector
python main.py help fav
python main.py help buy
python main.py help recommend
```

### Quick Start
```bash
# Show quick start guide
python main.py quick
```

### Version
```bash
# Show version and system info
python main.py version
```

## 💡 Usage Examples

### Daily Workflow

**Morning Routine:**
```bash
# 1. Check your portfolio
python main.py portfolio

# 2. Run daily scan
python main.py daily

# 3. Check favorites for signals
python main.py fav scan

# 4. Look at top opportunities
python main.py top 10
```

**Weekly Deep Dive:**
```bash
# 1. Scan AI companies
python main.py ai

# 2. Scan specific sectors
python main.py sector Fintech
python main.py sector "Cloud Computing"
python main.py sector "IT Services" --market INDIA

# 3. Check each market
python main.py india
python main.py canada
python main.py us
```

### Research Workflow

**Researching AI Stocks:**
```bash
# 1. Find AI companies
python main.py ai --market USA

# 2. Get quick info
python main.py info NVDA
python main.py info PLTR
python main.py info CRWD

# 3. Deep analysis
python main.py analyze NVDA
python main.py score NVDA

# 4. Evaluate buying
python main.py buy NVDA

# 5. Add to favorites
python main.py fav add NVDA ai
```

**Tracking Indian IT Services:**
```bash
# 1. Scan IT Services in India
python main.py sector "IT Services" --market INDIA

# 2. Check top performers
python main.py top 10 --market INDIA

# 3. Analyze individual stocks
python main.py analyze TCS.NS
python main.py analyze INFY.NS
python main.py analyze PERSISTENT.NS

# 4. Add promising ones to favorites
python main.py fav add TCS.NS india
python main.py fav add PERSISTENT.NS ai
```

### Building a Watchlist
```bash
# Add stocks to watchlist category
python main.py fav add NVDA watchlist
python main.py fav add PLTR watchlist
python main.py fav add TCS.NS watchlist
python main.py fav add SHOP.TO watchlist

# View watchlist
python main.py fav show watchlist

# Scan watchlist daily
python main.py fav scan
```

## 🎯 Tips & Tricks

### Efficient Scanning
```bash
# Focus on specific areas
python main.py ai --market USA --min-score 75          # High-quality US AI
python main.py sector Fintech --market INDIA          # Indian fintech
python main.py top 5 --market CANADA                  # Top Canadian stocks
```

### Quick Checks
```bash
# Fast info lookup
python main.py info NVDA        # Faster than full analyze
python main.py score PLTR       # Just the score breakdown
```

### Organize Favorites
```bash
# Organize by market
python main.py fav add NVDA usa
python main.py fav add TCS.NS india
python main.py fav add SHOP.TO canada

# Organize by sector
python main.py fav add CRWD tech
python main.py fav add VEEV healthcare
python main.py fav add SQ fintech

# Organize by strategy
python main.py fav add PLTR ai
python main.py fav add TSLA watchlist
```

### Command Chaining Workflow
```bash
# Morning routine
python main.py version                    # Check version
python main.py portfolio                  # Check portfolio
python main.py fav scan                   # Scan favorites
python main.py top 10                     # Top opportunities
python main.py daily                      # Full daily routine
```

## 📝 Symbol Formats

**US Stocks:**
```bash
python main.py analyze NVDA        # No suffix needed
python main.py analyze PLTR
python main.py analyze CRWD
```

**Canadian Stocks:**
```bash
python main.py analyze SHOP.TO     # .TO for TSX
python main.py analyze LSPD.TO
python main.py analyze NOU.V       # .V for TSXV
```

**Indian Stocks:**
```bash
python main.py analyze TCS.NS      # .NS for NSE (recommended)
python main.py analyze INFY.NS
python main.py analyze TCS.BO      # .BO for BSE (alternative)
```

## 🚦 Quick Reference Card

```bash
# Help & Info
help                        # Show all commands
help <command>              # Command-specific help
quick                       # Quick start guide
version                     # Version info

# Analysis
analyze <ticker>            # Full analysis
info <ticker>               # Quick info
score <ticker>              # Score breakdown
buy <ticker>                # Evaluate buying
sell <ticker>               # Evaluate selling

# Scanning
scan                        # General scan
ai                          # AI companies
ai --market <market>        # AI in specific market
sector <name>               # Scan sector
india/canada/us             # Market-specific

# Top Stocks
top <N>                     # Top N stocks
top <N> --market <market>   # Top N in market

# Favorites
fav                         # Show all favorites
fav add <ticker> <cat>      # Add to favorites
fav remove <ticker>         # Remove
fav show <cat>              # Show category
fav scan                    # Scan for signals
fav categories              # List categories
fav export <file>           # Export

# Portfolio
portfolio                   # Show portfolio
daily                       # Daily routine

# Recommendations
recommend                   # Get recommendations
recommend --focus <type>    # Focused recommendations
```

## 🆘 Need Help?

```bash
# General help
python main.py help

# Specific help
python main.py help analyze
python main.py help ai
python main.py help fav

# Quick start
python main.py quick

# Check version
python main.py version
```

---

**For complete documentation, see:**
- `README.md` - Full system documentation
- `AI_MARKETS_GUIDE.md` - AI companies and markets guide
- `QUICKSTART.md` - 5-minute setup guide
- `UPDATE_SUMMARY.md` - Latest updates

**Happy investing! 📈🚀**
