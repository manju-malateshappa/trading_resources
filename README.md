# Investment Agent 🤖📈

> **AI-powered investment analysis and portfolio management** - Available as a modern web application and powerful CLI tool.

## 🎯 What is This?

An intelligent system that helps you identify high-growth small/mid-cap stocks with potential for 100-200% returns. It combines:

- **Fundamental Analysis** - Deep dive into financials, growth metrics, and valuation
- **Technical Analysis** - Chart patterns, momentum indicators, trend analysis
- **Risk Management** - Position sizing, stop-loss, portfolio diversification
- **Portfolio Tracking** - Monitor positions, calculate returns, optimize allocation
- **Multi-Market Coverage** - USA (NASDAQ/NYSE), Canada (TSX), India (NSE)

---

## 🚀 Quick Start

### Option 1: Web Application (Full-Stack) 🌐

**Modern web interface with dashboard, charts, and real-time updates**

```bash
# 1. Start Backend (Terminal 1)
cd backend
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python3 -m uvicorn app.main:app --reload

# 2. Start Frontend (Terminal 2)
cd frontend
npm install
npm run dev

# 3. Open http://localhost:5173
```

**📚 Full Guide:** [Complete Setup Instructions](./docs/SETUP_GUIDE.md)

### Option 2: Command Line Tool (CLI) 💻

**Fast, scriptable interface for analysis and automation**

```bash
# 1. Setup
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r backend/requirements.txt

# 2. Run analysis
python3 cli.py analyze NVDA
python3 cli.py ai           # Scan AI companies
python3 cli.py portfolio    # View portfolio

# 3. Get help
python3 cli.py help
```

**📚 CLI Guide:** [CLI Reference](./docs/CLI_REFERENCE.md)

---

## ✨ Key Features

### Web Application
- ✅ **Secure Authentication** - JWT + Two-Factor Authentication (2FA)
- ✅ **Dashboard** - Portfolio overview with charts and metrics
- ✅ **Stock Search** - Real-time search with analysis
- ✅ **Portfolio Management** - Track positions, trades, and performance
- ✅ **Settings** - 2FA setup, profile management
- ✅ **Responsive Design** - Works on mobile, tablet, and desktop

### CLI Tool
- ✅ **Stock Analysis** - Deep dive into any stock (US/Canada/India)
- ✅ **Market Scanning** - Screen for opportunities across markets
- ✅ **Portfolio Tracking** - Manage multiple portfolios (TFSA, RRSP, etc.)
- ✅ **Favorites Management** - Track stocks by category
- ✅ **Cache System** - Fast repeated lookups
- ✅ **Rich Output** - Beautiful tables and colored output

### Analysis Capabilities
- 📊 **6-Factor Scoring** - Valuation, growth, profitability, health, quality, momentum
- 📈 **15+ Technical Indicators** - RSI, MACD, Bollinger Bands, ADX, and more
- 🎯 **Entry/Exit Signals** - Data-driven buy/sell recommendations
- 💰 **Position Sizing** - Kelly Criterion-based calculations
- 🛡️ **Risk Management** - Stop-loss, trailing stops, sector limits
- 🇨🇦 **Tax Optimization** - TFSA/RRSP/taxable account strategies

---

## 📁 Project Structure

```
trading_resources/
├── backend/              # FastAPI Backend
│   ├── app/
│   │   ├── api/v1/      # REST API endpoints
│   │   ├── models/      # Database models
│   │   ├── services/    # Business logic
│   │   └── main.py      # FastAPI application
│   └── requirements.txt
│
├── frontend/             # React Frontend
│   ├── src/
│   │   ├── pages/       # Login, Dashboard, Portfolio
│   │   ├── components/  # Reusable UI components
│   │   └── services/    # API client
│   └── package.json
│
├── docs/                 # Documentation
│   ├── SETUP_GUIDE.md   # Detailed setup instructions
│   ├── ARCHITECTURE.md  # System architecture
│   ├── CLI_REFERENCE.md # CLI commands guide
│   └── MARKETS_GUIDE.md # Market coverage & stock lists
│
└── cli.py               # CLI interface (original tool)
```

---

## 🔥 Web App Features

### Backend (FastAPI)
- ✅ **REST API** with automatic OpenAPI docs at `/docs`
- ✅ **JWT Authentication** with access and refresh tokens
- ✅ **Two-Factor Auth** (TOTP/Google Authenticator)
- ✅ **PostgreSQL/SQLite** for persistent storage
- ✅ **Session Management** with device tracking
- ✅ **Rate Limiting** and security hardening
- ✅ **Investment Logic** wrapped as API services

### Frontend (React + TypeScript)
- 📦 **Dashboard** - Portfolio overview and performance metrics
- 📦 **Stock Search** - Real-time search with autocomplete
- 📦 **Analysis Pages** - Charts, fundamentals, technicals
- 📦 **Portfolio UI** - Manage positions and trades
- 📦 **Settings** - 2FA setup, profile management
- 📦 **Responsive** - Mobile-first design

### API Endpoints

**Authentication:**
```
POST   /api/v1/auth/register    # Register new user
POST   /api/v1/auth/login       # Login (JWT tokens)
GET    /api/v1/auth/2fa/setup   # Setup 2FA
POST   /api/v1/auth/logout      # Logout
```

**Stocks (Coming Soon):**
```
GET    /api/v1/stocks/search         # Search stocks
GET    /api/v1/stocks/{symbol}       # Get stock details
GET    /api/v1/stocks/{symbol}/analyze  # Analyze stock
```

**Interactive Docs:** http://localhost:8000/docs (when backend running)

---

## 💻 CLI Examples

**Analyze a stock:**
```bash
python3 cli.py analyze NVDA
python3 cli.py analyze SHOP.TO    # Canadian stock
python3 cli.py analyze TCS.NS     # Indian stock
```

**Screen for opportunities:**
```bash
python3 cli.py ai           # Scan AI companies
python3 cli.py us           # US market scan
python3 cli.py canada       # Canadian market scan
python3 cli.py india        # Indian market scan
```

**Manage favorites:**
```bash
python3 cli.py fav add NVDA ai
python3 cli.py fav show
python3 cli.py fav scan     # Scan favorites for signals
```

**Portfolio management:**
```bash
python3 cli.py portfolio
python3 cli.py buy SHOP.TO
python3 cli.py sell LSPD.TO
```

**Data management:**
```bash
python3 cli.py list --market USA
python3 cli.py refresh --numbers 1-10
python3 cli.py cache stats
```

**📚 Full CLI Guide:** [CLI Reference](./docs/CLI_REFERENCE.md)

---

## 🏗️ Architecture

```
┌─────────────────────┐
│   React Frontend    │  ← User Interface
│   (TypeScript)      │
└──────────┬──────────┘
           │ HTTPS/REST
┌──────────▼──────────┐
│   FastAPI Backend   │  ← Business Logic + Auth
│   (Python 3.11+)    │
└──────────┬──────────┘
           │ SQL
┌──────────▼──────────┐
│   PostgreSQL DB     │  ← Data Storage
│   (or SQLite)       │
└─────────────────────┘
```

**Tech Stack:**
- **Backend:** FastAPI, SQLAlchemy, JWT, TOTP, bcrypt
- **Frontend:** React 18, TypeScript, Material-UI, React Query
- **Database:** PostgreSQL (production) / SQLite (development)
- **Deployment:** Vercel (frontend) + Railway (backend) + Supabase (DB)

**📚 Deep Dive:** [Architecture Documentation](./docs/ARCHITECTURE.md)

---

## 🔐 Security Features

- ✅ **Password Hashing** - bcrypt with 12 rounds
- ✅ **JWT Tokens** - Access (30min) + Refresh (7 days)
- ✅ **Two-Factor Auth** - TOTP with QR codes
- ✅ **Session Tracking** - IP, device, user agent logging
- ✅ **Rate Limiting** - Prevent brute force attacks
- ✅ **Account Locking** - After 5 failed login attempts
- ✅ **Encrypted Secrets** - TOTP secrets encrypted at rest

---

## 📊 Investment Strategy

### Entry Criteria (Configurable)
- Revenue Growth: >15% YoY
- P/E Ratio: <30 (flexible for high-growth)
- Profit Margin: >5%
- Market Cap: $100M - $10B (small/mid-cap focus)
- Average Volume: >50,000 shares/day

### Exit Strategy
**Take-Profit Levels:**
- 25% gain → Sell 20% of position
- 50% gain → Sell 25% of position
- 100% gain → Sell 30% of position
- 200% gain → Sell remaining position

**Stop-Loss:**
- 15% fixed stop-loss
- 10% trailing stop after 20% gain

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [Setup Guide](./docs/SETUP_GUIDE.md) | Complete setup walkthrough (2-4 hours) |
| [Architecture](./docs/ARCHITECTURE.md) | System design and tech stack |
| [CLI Reference](./docs/CLI_REFERENCE.md) | All CLI commands and examples |
| [Markets Guide](./docs/MARKETS_GUIDE.md) | Market coverage and stock lists |
| [Backend README](./backend/README.md) | Backend-specific documentation |

---

## 🌍 Market Coverage

### 🇺🇸 USA
- **Exchanges:** NASDAQ, NYSE
- **Companies:** 200+ including NVIDIA, Palantir, Microsoft, etc.
- **Sectors:** AI, Cloud, Cybersecurity, Fintech, EV, Biotech

### 🇨🇦 Canada
- **Exchanges:** TSX, TSXV
- **Companies:** 50+ including Shopify, Lightspeed, etc.
- **Sectors:** Technology, Healthcare, Clean Energy, Cannabis

### 🇮🇳 India
- **Exchanges:** NSE, BSE
- **Companies:** 100+ including TCS, Infosys, Wipro, etc.
- **Sectors:** IT Services, Fintech, E-commerce, Pharma, EV

**📚 Full List:** [Markets Guide](./docs/MARKETS_GUIDE.md)

---

## 🇨🇦 Canadian Tax Optimization

### TFSA (Tax-Free Savings Account)
- **Best for:** High-growth stocks (100%+ gains)
- **Tax on gains:** 0%
- **Strategy:** Prioritize stocks with 100-200% return potential

### RRSP (Registered Retirement Savings Plan)
- **Best for:** Dividend-paying stocks
- **Tax benefit:** Deduction on contribution
- **Strategy:** Stable, dividend-focused holdings

### Taxable Account
- **Capital gains:** 50% inclusion rate
- **Tax-loss harvesting:** Offset gains with losses
- **Superficial loss rule:** Wait 30 days before repurchasing

---

## 🛠️ Development Roadmap

### ✅ Completed
- [x] Backend foundation with FastAPI
- [x] JWT + 2FA authentication
- [x] Database models (User, Session, Portfolio)
- [x] CLI tool with full analysis capabilities
- [x] Multi-market stock database (200+ companies)
- [x] Fundamental & technical analysis engines

### 📅 In Progress (Week 2)
- [ ] Stock analysis API endpoints
- [ ] Portfolio management API
- [ ] Redis caching layer
- [ ] Background job processing

### 📅 Planned (Weeks 3-4)
- [ ] Frontend dashboard
- [ ] Real-time stock data
- [ ] Charts and visualizations
- [ ] Mobile responsiveness
- [ ] Production deployment

---

## 🧪 Testing

### Test Backend
```bash
cd backend
source venv/bin/activate
python3 -m pytest tests/ -v
```

### Test CLI
```bash
# Quick smoke test
python3 cli.py help
python3 cli.py analyze NVDA
python3 cli.py list --market USA | head -20
```

### Test API (with backend running)
```bash
# Health check
curl http://localhost:8000/health

# API docs
open http://localhost:8000/docs
```

---

## 🐛 Troubleshooting

### Backend won't start
```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
python3 -m uvicorn app.main:app --reload
```

### Database connection error
```bash
# Check .env file
cat backend/.env

# For local development, use SQLite:
DATABASE_URL=sqlite:///./investment_agent.db
```

### CLI import errors
```bash
# Make sure dependencies are installed
pip install -r backend/requirements.txt

# Check Python version (need 3.11+)
python3 --version
```

**📚 More Help:** [Setup Guide](./docs/SETUP_GUIDE.md#troubleshooting)

---

## 🛡️ Risk Disclaimer

**IMPORTANT:** This software is for educational and research purposes only.

- ❌ **Not Financial Advice** - Always do your own research
- ❌ **No Guarantees** - Past performance doesn't guarantee future results
- ⚠️ **High Risk** - Small/mid-cap stocks are volatile
- ✅ **Paper Trade First** - Test before using real money
- ✅ **Consult Professionals** - Talk to licensed financial advisors
- ✅ **Know Your Limits** - Only invest what you can afford to lose

---

## 📧 Support

- **Documentation:** Check `docs/` folder
- **CLI Help:** `python3 cli.py help`
- **API Docs:** http://localhost:8000/docs (when running)
- **Issues:** Create an issue on GitHub

---

## 🎯 Quick Reference

**Web App:**
```bash
# Backend
cd backend && uvicorn app.main:app --reload

# Frontend
cd frontend && npm run dev
```

**CLI:**
```bash
# Analysis
python3 cli.py analyze NVDA
python3 cli.py ai
python3 cli.py portfolio

# Data management
python3 cli.py list
python3 cli.py refresh --numbers 1-10
python3 cli.py cache stats
```

**Documentation:**
- [Setup Guide](./docs/SETUP_GUIDE.md) - Getting started
- [Architecture](./docs/ARCHITECTURE.md) - System design
- [CLI Reference](./docs/CLI_REFERENCE.md) - All commands
- [Markets Guide](./docs/MARKETS_GUIDE.md) - Stock coverage

---

**Happy Investing! 🚀📈**

*Remember: The best investment is in your own knowledge. Always keep learning!*
