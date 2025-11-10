# Investment Agent API - Backend

FastAPI-based backend for the Investment Agent full-stack application.

## 🏗️ Technology Stack

- **Framework**: FastAPI 0.104+
- **Database**: PostgreSQL (via Supabase)
- **ORM**: SQLAlchemy 2.0+
- **Authentication**: JWT + 2FA (TOTP)
- **Cache**: Redis (optional, via Upstash)
- **Deployment**: Railway / Render / AWS

## 📁 Project Structure

```
backend/
├── app/
│   ├── api/
│   │   └── v1/          # API endpoints (versioned)
│   │       ├── auth.py  # Authentication
│   │       ├── stocks.py
│   │       ├── portfolio.py
│   │       └── analysis.py
│   ├── core/
│   │   └── security.py  # Security utilities (JWT, 2FA, encryption)
│   ├── models/          # SQLAlchemy models
│   │   ├── user.py
│   │   ├── session.py
│   │   └── portfolio.py
│   ├── schemas/         # Pydantic schemas
│   │   ├── auth.py
│   │   └── user.py
│   ├── services/        # Business logic
│   │   └── investment_agent/  # Original CLI agent code
│   ├── utils/           # Helper functions
│   ├── config.py        # Configuration management
│   ├── database.py      # Database connection
│   └── main.py          # FastAPI app
├── tests/               # Pytest tests
├── .env                 # Environment variables (NOT in git)
├── .env.example         # Environment template
└── requirements.txt     # Python dependencies
```

## 🚀 Quick Start

### 1. Prerequisites

- Python 3.11+
- PostgreSQL database (or Supabase account)
- Redis (optional, for caching)

### 2. Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env

# Edit .env with your configuration
nano .env  # or your preferred editor
```

### 3. Configure Environment Variables

Edit `.env` file:

```bash
# Required
SECRET_KEY=your-secret-key-here  # Generate with: openssl rand -hex 32
DATABASE_URL=postgresql://user:password@localhost:5432/investment_agent

# Optional
REDIS_URL=redis://localhost:6379/0
ALPHA_VANTAGE_API_KEY=your_key
FINNHUB_API_KEY=your_key
```

### 4. Initialize Database

```bash
# Run migrations (creates tables)
python3 -m app.main

# Or use Alembic for migrations
alembic upgrade head
```

### 5. Run Development Server

```bash
# Start server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# OR
python3 -m app.main
```

Server will be available at:
- API: http://localhost:8000
- Docs: http://localhost:8000/docs
- Health: http://localhost:8000/health

## 📚 API Documentation

### Authentication Endpoints

#### Register
```bash
POST /api/v1/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "username": "johndoe",
  "password": "SecurePass123",
  "full_name": "John Doe"
}
```

#### Login
```bash
POST /api/v1/auth/login
Content-Type: application/json

{
  "username_or_email": "johndoe",
  "password": "SecurePass123"
}

# Response (if 2FA disabled):
{
  "access_token": "eyJ...",
  "refresh_token": "eyJ...",
  "token_type": "bearer",
  "user": {...}
}

# Response (if 2FA enabled):
{
  "requires_2fa": true,
  "temp_token": "eyJ...",
  "message": "Please enter your 2FA code"
}
```

#### Setup 2FA
```bash
GET /api/v1/auth/2fa/setup
Authorization: Bearer <access_token>

# Response:
{
  "secret": "JBSWY3DPEHPK3PXP",
  "qr_code": "data:image/png;base64,...",
  "backup_codes": ["ABCD-1234", ...]
}
```

### Interactive API Docs

Visit `http://localhost:8000/docs` for interactive Swagger UI documentation.

## 🔐 Security Features

### Authentication
- ✅ JWT access tokens (30 min expiry)
- ✅ Refresh tokens (7 day expiry)
- ✅ Password hashing with bcrypt (12 rounds)
- ✅ Rate limiting (5 login attempts / 15 min)
- ✅ Account locking after failed attempts

### 2FA (Two-Factor Authentication)
- ✅ TOTP (Time-based One-Time Password)
- ✅ QR code generation for authenticator apps
- ✅ Backup codes for recovery
- ✅ Encrypted storage of TOTP secrets

### Session Management
- ✅ Device tracking (IP, user agent)
- ✅ Active session list
- ✅ "Logout all devices" functionality
- ✅ Session expiration

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app tests/

# Run specific test file
pytest tests/test_auth.py

# Run with verbose output
pytest -v
```

## 📦 Database Migrations

Using Alembic:

```bash
# Create a new migration
alembic revision --autogenerate -m "Add new field to user table"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1

# View migration history
alembic history
```

## 🚀 Deployment

### Environment Variables for Production

```bash
ENVIRONMENT=production
DEBUG=false
SECRET_KEY=<strong-random-key>
DATABASE_URL=<production-db-url>
BACKEND_CORS_ORIGINS=https://yourapp.com,https://www.yourapp.com
```

### Deploy to Railway

1. Connect GitHub repo to Railway
2. Set environment variables in Railway dashboard
3. Railway auto-deploys on git push

### Deploy to Render

1. Create new Web Service in Render
2. Connect GitHub repo
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

## 🐛 Troubleshooting

### Database Connection Error
```bash
# Check DATABASE_URL format
DATABASE_URL=postgresql://user:password@host:port/dbname

# Test connection
python3 -c "from app.database import check_db_connection; print(check_db_connection())"
```

### Import Errors
```bash
# Make sure you're in backend directory and venv is activated
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Reinstall dependencies
pip install -r requirements.txt
```

### Port Already in Use
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Or use different port
uvicorn app.main:app --port 8001
```

## 📝 Development

### Adding New Endpoints

1. Create router in `app/api/v1/`
2. Add schemas in `app/schemas/`
3. Add models if needed in `app/models/`
4. Register router in `app/main.py`

Example:
```python
# app/api/v1/stocks.py
from fastapi import APIRouter

router = APIRouter()

@router.get("/search")
async def search_stocks(query: str):
    return {"results": []}

# app/main.py
from app.api.v1 import stocks
app.include_router(stocks.router, prefix="/api/v1/stocks", tags=["stocks"])
```

## 🔗 Useful Links

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Supabase Documentation](https://supabase.com/docs)
- [Pydantic Documentation](https://docs.pydantic.dev/)

## 📧 Support

For issues or questions, please create an issue in the GitHub repository.

---

**Happy Coding! 🚀**
