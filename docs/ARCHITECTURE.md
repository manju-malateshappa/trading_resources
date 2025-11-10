# Investment Agent - System Architecture

## 🏛️ Overview

The Investment Agent is a full-stack web application that provides AI-powered investment analysis and portfolio management. The system follows a modern three-tier architecture with a React frontend, FastAPI backend, and PostgreSQL database.

## 📊 High-Level Architecture

```
┌─────────────────────────────────────────────────────┐
│         FRONTEND (User Interface)                   │
│  React + Material-UI + TanStack Query              │
│  - Dashboard, Portfolio, Stock Analysis            │
│  - Real-time updates, Charts, Notifications        │
└──────────────────┬──────────────────────────────────┘
                   │ HTTPS/WSS
┌──────────────────▼──────────────────────────────────┐
│         BACKEND API (Business Logic)                │
│  FastAPI + SQLAlchemy + Investment Agent            │
│  - Authentication (JWT + 2FA)                       │
│  - Stock Analysis & Screening                       │
│  - Portfolio Management                             │
│  - Real-time Stock Data                             │
└──────────────────┬──────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────┐
│         DATABASE (Data Storage)                     │
│  PostgreSQL (via Supabase)                          │
│  - Users, Sessions, Portfolios                      │
│  - Trades, Positions, Watchlists                    │
└──────────────────┬──────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────┐
│         CACHE/QUEUE (Performance)                   │
│  Redis (via Upstash)                                │
│  - Stock data cache (1h TTL)                        │
│  - Session storage                                  │
│  - Background job queue                             │
└─────────────────────────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────┐
│         EXTERNAL APIs                               │
│  - Yahoo Finance (yfinance)                         │
│  - Alpha Vantage                                    │
│  - Finnhub                                          │
│  - FRED Economic Data                               │
└─────────────────────────────────────────────────────┘
```

## 🎯 Core Components

### 1. Frontend (React)

**Technology Stack:**
- React 18+ (with hooks)
- TypeScript
- Material-UI / Tailwind CSS
- TanStack Query (React Query) for data fetching
- Recharts / Chart.js for visualizations
- React Router for navigation
- Zustand / Context API for state management

**Key Features:**
- Responsive design (mobile, tablet, desktop)
- Real-time stock price updates
- Interactive charts and dashboards
- Dark/light theme
- Progressive Web App (PWA) capabilities

**Pages:**
- `/` - Landing page
- `/login` - Login with 2FA
- `/register` - User registration
- `/dashboard` - Main dashboard with portfolio overview
- `/portfolio` - Detailed portfolio management
- `/stocks/search` - Stock search and screening
- `/stocks/:symbol` - Individual stock analysis
- `/settings` - User settings and 2FA

### 2. Backend (FastAPI)

**Technology Stack:**
- FastAPI (async Python framework)
- SQLAlchemy 2.0 (async ORM)
- Pydantic (data validation)
- PostgreSQL (database)
- Redis (caching)
- Celery (background tasks)

**Core Modules:**

#### A. Authentication & Security
- JWT-based authentication
- 2FA with TOTP (Google Authenticator)
- Password hashing (bcrypt)
- Session management
- Rate limiting
- CORS protection

#### B. Investment Agent Service
Located in `backend/app/services/investment_agent/`

**Original CLI Components (now as services):**
- `data_fetcher.py` - Fetch stock data from APIs
- `fundamental_analyzer.py` - Fundamental analysis
- `technical_analyzer.py` - Technical analysis
- `stock_screener.py` - Screen stocks by criteria
- `portfolio_manager.py` - Portfolio operations
- `risk_manager.py` - Risk assessment

**New API Wrappers:**
- `stock_service.py` - Wraps stock operations for API
- `portfolio_service.py` - Wraps portfolio operations
- `analysis_service.py` - Wraps analysis operations

#### C. API Endpoints (RESTful)

**Auth Routes** (`/api/v1/auth/*`):
- `POST /register` - User registration
- `POST /login` - User login
- `POST /verify-2fa` - 2FA verification
- `GET /2fa/setup` - Setup 2FA
- `POST /2fa/enable` - Enable 2FA
- `POST /logout` - Logout
- `POST /refresh` - Refresh token

**User Routes** (`/api/v1/users/*`):
- `GET /me` - Get current user
- `PUT /me` - Update profile
- `POST /change-password` - Change password

**Stock Routes** (`/api/v1/stocks/*`):
- `GET /search?q={query}` - Search stocks
- `GET /{symbol}` - Get stock info
- `GET /{symbol}/analysis` - Full stock analysis
- `GET /{symbol}/price` - Real-time price
- `GET /{symbol}/chart` - Historical data
- `POST /screen` - Screen stocks

**Portfolio Routes** (`/api/v1/portfolio/*`):
- `GET /` - List user portfolios
- `POST /` - Create portfolio
- `GET /{id}` - Get portfolio details
- `GET /{id}/positions` - Get positions
- `POST /{id}/buy` - Execute buy
- `POST /{id}/sell` - Execute sell
- `GET /{id}/performance` - Performance metrics

**Analysis Routes** (`/api/v1/analysis/*`):
- `POST /evaluate` - Evaluate buy/sell decision
- `GET /opportunities` - Find opportunities
- `GET /recommendations` - Get recommendations

### 3. Database (PostgreSQL)

**Schema Design:**

#### Users Table
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(50) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE,
    is_verified BOOLEAN DEFAULT FALSE,
    is_2fa_enabled BOOLEAN DEFAULT FALSE,
    totp_secret VARCHAR(255),  -- Encrypted
    backup_codes TEXT,  -- JSON array
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

#### Sessions Table
```sql
CREATE TABLE sessions (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    session_token VARCHAR(255) UNIQUE,
    refresh_token VARCHAR(255) UNIQUE,
    user_agent VARCHAR(500),
    ip_address VARCHAR(45),
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);
```

#### Portfolios Table
```sql
CREATE TABLE portfolios (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    name VARCHAR(100) NOT NULL,
    portfolio_type VARCHAR(20),  -- tfsa, rrsp, taxable, paper
    initial_cash DECIMAL(15,2),
    current_cash DECIMAL(15,2),
    total_value DECIMAL(15,2),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW()
);
```

#### Positions & Trades Tables
(See `backend/app/models/portfolio.py` for full schema)

### 4. Cache Layer (Redis)

**Cache Keys Structure:**
```
stock:{symbol}:info          # Stock info (TTL: 1h)
stock:{symbol}:price         # Real-time price (TTL: 1min)
stock:{symbol}:analysis      # Analysis results (TTL: 24h)
user:{user_id}:session       # Session data (TTL: 24h)
market:opportunities         # Market opportunities (TTL: 1h)
```

**Usage:**
- Reduce API calls to external services
- Cache analysis results
- Session storage
- Rate limiting counters

## 🔄 Data Flow

### User Login Flow
```
1. User submits credentials
   ↓
2. Backend validates password
   ↓
3. If 2FA enabled → Send temp token
   ↓
4. User submits 2FA code
   ↓
5. Backend verifies TOTP
   ↓
6. Generate JWT tokens
   ↓
7. Create session in DB + Redis
   ↓
8. Return tokens to frontend
   ↓
9. Frontend stores tokens (httpOnly cookies or localStorage)
```

### Stock Analysis Flow
```
1. User requests analysis for AAPL
   ↓
2. Check Redis cache
   ├─ Hit → Return cached result
   └─ Miss ↓
3. Fetch data from yfinance/Alpha Vantage
   ↓
4. Run fundamental analysis
   ↓
5. Run technical analysis
   ↓
6. Calculate investment score
   ↓
7. Store in Redis (24h TTL)
   ↓
8. Return to frontend
```

### Buy/Sell Trade Flow
```
1. User requests buy 100 shares of AAPL
   ↓
2. Validate portfolio has cash
   ↓
3. Get current price from cache/API
   ↓
4. Create trade record in DB
   ↓
5. Update/create position
   ↓
6. Update portfolio cash & value
   ↓
7. Trigger position update background job
   ↓
8. Return confirmation to frontend
```

## 🔐 Security Architecture

### Authentication Flow
1. **Registration**: Password hashed with bcrypt (12 rounds)
2. **Login**: JWT access token (30 min) + refresh token (7 days)
3. **2FA**: TOTP stored encrypted, verified on login
4. **Session**: Tracked in DB with device info, IP address

### Authorization
- Role-based access control (future)
- Resource ownership validation
- Rate limiting per endpoint

### Data Protection
- Passwords: bcrypt hashing
- TOTP secrets: AES encryption
- Tokens: JWT with HS256
- HTTPS: TLS 1.3 in production
- CORS: Whitelist frontend domains

## 📈 Scalability

### Current (MVP)
- Single server deployment
- PostgreSQL single instance
- Redis single instance
- Handles ~100 concurrent users

### Future (Growth)
- Horizontal scaling with load balancer
- Database read replicas
- Redis cluster
- CDN for static assets
- Background job workers (Celery)
- WebSocket for real-time updates

## 🚀 Deployment Architecture

### Development
```
Local Machine
├── Frontend: localhost:3000 (Vite dev server)
└── Backend: localhost:8000 (uvicorn --reload)
```

### Production
```
Vercel (Frontend)
├── Static assets on CDN
└── API calls to → Railway (Backend)
                   ├── FastAPI app
                   ├── Celery workers
                   └── Connects to:
                       ├── Supabase (PostgreSQL)
                       └── Upstash (Redis)
```

## 🔧 Technology Decisions

### Why FastAPI?
- ✅ Async support (better performance)
- ✅ Automatic API docs (Swagger/OpenAPI)
- ✅ Type hints and validation (Pydantic)
- ✅ Easy to learn and fast development

### Why PostgreSQL?
- ✅ ACID compliance (data integrity)
- ✅ Rich feature set (JSON, full-text search)
- ✅ Excellent SQLAlchemy support
- ✅ Supabase provides free tier

### Why Redis?
- ✅ Ultra-fast caching
- ✅ Session storage
- ✅ Pub/sub for real-time features
- ✅ Upstash provides free tier

### Why React?
- ✅ Large ecosystem and community
- ✅ Component reusability
- ✅ Excellent developer tools
- ✅ Easy integration with charts/UI libraries

## 📊 Monitoring & Observability

### Logging
- Structured logging with loguru
- Log levels: DEBUG, INFO, WARNING, ERROR
- Request/response logging
- Error tracking

### Metrics (Future)
- Prometheus + Grafana
- API response times
- Database query performance
- Cache hit rates
- Active users

### Alerting (Future)
- PagerDuty / Sentry
- Error rate thresholds
- API latency alerts
- Database connection issues

## 🔄 CI/CD Pipeline

```
Git Push
  ↓
GitHub Actions
  ├── Run tests (pytest)
  ├── Lint code (black, flake8)
  ├── Security scan
  ↓
Deploy
  ├── Frontend → Vercel (automatic)
  └── Backend → Railway (automatic)
```

## 📚 Additional Resources

- [API Documentation](./API.md)
- [Setup Guide](./SETUP_GUIDE.md)
- [Deployment Guide](./DEPLOYMENT.md)

---

**Last Updated**: Week 1 - Backend Foundation Phase
