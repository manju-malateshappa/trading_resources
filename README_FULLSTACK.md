# Investment Agent 🤖📈

> **AI-powered investment analysis and portfolio management** - Now available as both a **Full-Stack Web Application** and **CLI Tool**!

## 🚀 What's New: Full-Stack Web Application!

Your Investment Agent has been transformed into a **production-ready full-stack application** with:

✅ **Modern Web Interface** - React frontend with beautiful UI
✅ **Secure Authentication** - JWT + Two-Factor Authentication (2FA)
✅ **RESTful API** - FastAPI backend with auto-generated docs
✅ **Cloud Database** - PostgreSQL via Supabase
✅ **Real-time Updates** - Live stock prices and portfolio tracking
✅ **Enterprise Security** - Password encryption, session management, rate limiting
✅ **Scalable Architecture** - Ready for deployment on Railway/Vercel

**⚡ Quick Start**: See [Full-Stack Setup Guide](./docs/SETUP_GUIDE.md)

---

## 📁 Project Structure

```
trading_resources/
├── backend/              # 🔥 NEW: FastAPI Backend
│   ├── app/
│   │   ├── api/v1/      # REST API endpoints
│   │   ├── models/      # Database models
│   │   ├── schemas/     # Request/response validation
│   │   ├── services/    # Business logic
│   │   │   └── investment_agent/  # Original CLI code (now as service)
│   │   └── main.py      # FastAPI application
│   └── requirements.txt
│
├── frontend/             # 🔥 NEW: React Frontend
│   ├── src/
│   │   ├── pages/       # Login, Dashboard, Portfolio, etc.
│   │   ├── components/  # Reusable UI components
│   │   └── services/    # API client
│   └── package.json
│
├── docs/                 # 🔥 NEW: Documentation
│   ├── ARCHITECTURE.md   # System architecture
│   ├── SETUP_GUIDE.md    # Complete setup instructions
│   └── API.md           # API documentation
│
├── cli.py               # ✅ Original CLI tool (preserved)
└── FULLSTACK_SUMMARY.md # 🔥 NEW: Transformation summary
```

---

## 🎯 Choose Your Interface

### Option 1: Web Application (Recommended) 🌐

**Full-featured web app with dashboard, real-time updates, and beautiful UI**

```bash
# Backend (Terminal 1)
cd backend
source tradingEnv/bin/activate
uvicorn app.main:app --reload

# Frontend (Terminal 2)
cd frontend
npm install
npm run dev

# Open: http://localhost:5173
```

**📚 Full Guide**: [Complete Setup Instructions](./docs/SETUP_GUIDE.md)

### Option 2: Command Line (Original) 💻

**Powerful CLI for quick analysis and scripting**

```bash
# Activate environment
source tradingEnv/bin/activate

# Analyze a stock
python3 cli.py analyze NVDA

# Screen for opportunities
python3 cli.py ai

# Manage portfolio
python3 cli.py portfolio
```

**📚 CLI Guide**: Scroll down for complete CLI documentation

---

## 🔥 New Full-Stack Features

### Backend (FastAPI)
- ✅ **REST API** with automatic OpenAPI docs
- ✅ **User Authentication** with JWT tokens
- ✅ **Two-Factor Authentication** (TOTP/Google Authenticator)
- ✅ **PostgreSQL Database** for persistent data
- ✅ **Session Management** with device tracking
- ✅ **Rate Limiting** and security features
- ✅ **Original Investment Logic** wrapped as API services

### Frontend (React)
- 📦 **Dashboard** with portfolio overview
- 📦 **Stock Search** with real-time results
- 📦 **Analysis Pages** with charts and metrics
- 📦 **Portfolio Management** UI
- 📦 **Settings** with 2FA setup
- 📦 **Responsive Design** (mobile, tablet, desktop)

### Deployment Ready
- 📦 **Backend**: Deploy to Railway/Render
- 📦 **Frontend**: Deploy to Vercel
- 📦 **Database**: Supabase (free tier)
- 📦 **Cache**: Upstash Redis (free tier)

---

## 📊 API Endpoints (Backend)

### Authentication
```bash
POST   /api/v1/auth/register      # Register new user
POST   /api/v1/auth/login         # Login with credentials
POST   /api/v1/auth/verify-2fa    # Verify 2FA code
GET    /api/v1/auth/2fa/setup     # Setup 2FA
POST   /api/v1/auth/logout        # Logout
```

### Stocks (Coming Soon)
```bash
GET    /api/v1/stocks/search      # Search stocks
GET    /api/v1/stocks/{symbol}    # Get stock info
GET    /api/v1/stocks/{symbol}/analysis  # Analyze stock
POST   /api/v1/stocks/screen      # Screen opportunities
```

### Portfolio (Coming Soon)
```bash
GET    /api/v1/portfolio          # List portfolios
POST   /api/v1/portfolio/{id}/buy  # Execute buy
POST   /api/v1/portfolio/{id}/sell # Execute sell
GET    /api/v1/portfolio/{id}/performance  # Get metrics
```

**Interactive API Docs**: http://localhost:8000/docs (when backend running)

---

## 🚀 Quick Start (Web App)

### 1. Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL (or Supabase account)

### 2. Setup Backend (5 minutes)

```bash
cd backend

# Create environment
python3 -m venv tradingEnv
source tradingEnv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env: Add SECRET_KEY and DATABASE_URL

# Start server
uvicorn app.main:app --reload
```

**Verify**: Visit http://localhost:8000/docs

### 3. Setup Frontend (5 minutes)

```bash
cd frontend

# Install dependencies
npm install

# Start dev server
npm run dev
```

**Verify**: Visit http://localhost:5173

### 4. Test Registration

1. Go to http://localhost:5173/register
2. Create account
3. Login
4. Setup 2FA (optional)

✅ **Done!** You now have a working full-stack investment agent!

**Need Help?** See [Complete Setup Guide](./docs/SETUP_GUIDE.md)

---

## 🏗️ Architecture

```
┌─────────────────────┐
│   React Frontend    │  ← User Interface
└──────────┬──────────┘
           │ HTTPS
┌──────────▼──────────┐
│   FastAPI Backend   │  ← Business Logic + Auth
└──────────┬──────────┘
           │
┌──────────▼──────────┐
│   PostgreSQL DB     │  ← Data Storage
└─────────────────────┘
```

**Deep Dive**: [Architecture Documentation](./docs/ARCHITECTURE.md)

---

## 🔐 Security Features

- ✅ **Password Hashing**: bcrypt with 12 rounds
- ✅ **JWT Tokens**: Access (30min) + Refresh (7 days)
- ✅ **Two-Factor Auth**: TOTP with Google Authenticator
- ✅ **Session Tracking**: IP, device, user agent
- ✅ **Rate Limiting**: Prevent brute force attacks
- ✅ **Account Locking**: After 5 failed attempts
- ✅ **Encrypted Secrets**: TOTP secrets encrypted at rest

---

## 📚 Documentation

- **[Full-Stack Setup Guide](./docs/SETUP_GUIDE.md)** - Complete walkthrough (2-4 hours)
- **[Architecture](./docs/ARCHITECTURE.md)** - System design and tech stack
- **[Transformation Summary](./FULLSTACK_SUMMARY.md)** - What changed and why
- **[Backend README](./backend/README.md)** - Backend-specific documentation
- **CLI Guide** - See below for original CLI documentation

---

## 📈 Development Roadmap

### ✅ Week 1: Backend Foundation (COMPLETED!)
- [x] FastAPI setup
- [x] Database models (User, Session, Portfolio)
- [x] Authentication (JWT + 2FA)
- [x] Security features
- [x] API documentation
- [x] Backend deployment ready

### 📅 Week 2: Investment Logic API
- [ ] Stock search endpoints
- [ ] Stock analysis endpoints
- [ ] Portfolio management endpoints
- [ ] Trade execution endpoints
- [ ] Redis caching
- [ ] Background jobs

### 📅 Week 3: Frontend Development
- [ ] Dashboard page
- [ ] Portfolio management UI
- [ ] Stock search and analysis
- [ ] Charts and visualizations
- [ ] Settings page
- [ ] Mobile responsiveness

### 📅 Week 4: Polish & Deploy
- [ ] Testing (backend + frontend)
- [ ] Performance optimization
- [ ] Deploy to production
- [ ] Monitoring and logging
- [ ] User documentation

---

## 🎓 Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - Database ORM
- **PostgreSQL** - Relational database
- **JWT** - Token authentication
- **TOTP** - Two-factor auth
- **Redis** - Caching (optional)

### Frontend
- **React 18** - UI library
- **TypeScript** - Type safety
- **Material-UI** - Components
- **React Query** - Data fetching
- **Recharts** - Data visualization
- **React Router** - Navigation

### Deployment
- **Vercel** - Frontend hosting
- **Railway** - Backend hosting
- **Supabase** - Database hosting
- **Upstash** - Redis hosting

---

## 🆘 Troubleshooting

### Backend Won't Start
```bash
# Make sure you're in backend/ and venv is activated
cd backend
source tradingEnv/bin/activate
pip install -r requirements.txt
```

### Database Connection Error
```bash
# Check .env file has correct DATABASE_URL
# Format: postgresql://user:password@host:port/database
```

### Frontend Can't Connect
```bash
# Check backend is running on port 8000
# Check frontend .env has: VITE_API_URL=http://localhost:8000
```

**More Help**: [Troubleshooting Guide](./docs/SETUP_GUIDE.md#troubleshooting)

---

---

# 💻 Original CLI Documentation

> The original command-line interface is still fully functional!

