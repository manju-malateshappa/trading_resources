# Investment Agent - Complete Setup Guide

This guide walks you through setting up the Investment Agent full-stack application from scratch.

## ⏱️ Estimated Time

- **Backend Setup**: 1-2 hours
- **Frontend Setup**: 1-2 hours
- **Total**: 2-4 hours

## 📋 Prerequisites

### Required
- Python 3.11+ installed
- Node.js 18+ installed
- Git installed
- Code editor (VS Code recommended)
- Terminal/Command Line access

### Accounts (Free Tier Available)
- GitHub account
- Supabase account (for database)
- Vercel account (for frontend hosting)
- Railway account (for backend hosting)

## 🎯 Part 1: Backend Setup (Week 1, Day 1)

### Step 1: Project Setup (10 min)

```bash
# Clone repository
git clone <your-repo-url>
cd trading_resources

# Navigate to backend
cd backend

# Create virtual environment
python3 -m venv tradingEnv
source tradingEnv/bin/activate  # On Windows: tradingEnv\Scripts\activate

# Verify Python version
python --version  # Should be 3.11+
```

### Step 2: Install Dependencies (10 min)

```bash
# Install all backend dependencies
pip install -r requirements.txt

# Verify installation
pip list | grep fastapi
pip list | grep sqlalchemy
```

**If installation fails:**
```bash
# Install core packages individually
pip install fastapi uvicorn sqlalchemy psycopg2-binary
pip install python-jose passlib bcrypt pyotp qrcode
pip install pandas numpy yfinance
```

### Step 3: Database Setup - Supabase (20 min)

1. **Create Supabase Project:**
   - Go to [supabase.com](https://supabase.com)
   - Click "Start your project"
   - Create new organization
   - Create new project:
     - Name: `investment-agent`
     - Database Password: Save this securely!
     - Region: Choose closest to you

2. **Get Database Connection String:**
   - Go to Project Settings → Database
   - Copy "Connection string" (URI format)
   - Example: `postgresql://postgres:password@db.xxx.supabase.co:5432/postgres`

3. **Test Connection:**
```bash
# Install psql if not available
# macOS: brew install postgresql
# Ubuntu: sudo apt-get install postgresql-client

# Test connection
psql "postgresql://postgres:password@db.xxx.supabase.co:5432/postgres"

# Should connect successfully
# Type \q to exit
```

### Step 4: Configure Environment Variables (10 min)

```bash
# Copy environment template
cp .env.example .env

# Edit .env file
nano .env  # or code .env for VS Code
```

**Required Configuration:**
```bash
# Generate SECRET_KEY
openssl rand -hex 32

# Copy output and paste in .env:
SECRET_KEY=<paste-generated-key-here>

# Add your Supabase database URL
DATABASE_URL=postgresql://postgres:password@db.xxx.supabase.co:5432/postgres

# Optional: Add API keys (can be added later)
ALPHA_VANTAGE_API_KEY=
FINNHUB_API_KEY=
```

### Step 5: Initialize Database (10 min)

```bash
# Run FastAPI app (this will create tables)
uvicorn app.main:app --reload

# You should see:
# ✓ Database tables created
# ✓ Investment Agent API v1.0.0 started successfully
```

**Verify Tables Created:**
```bash
# Open Supabase dashboard
# Go to Table Editor
# You should see: users, sessions, portfolios, positions, trades
```

### Step 6: Test Backend API (10 min)

1. **Open API Documentation:**
   - Navigate to: http://localhost:8000/docs
   - You should see Swagger UI

2. **Test Health Endpoint:**
   ```bash
   curl http://localhost:8000/health

   # Expected response:
   # {"status":"healthy","database":"connected","version":"1.0.0"}
   ```

3. **Test User Registration:**
   - In Swagger UI, expand `POST /api/v1/auth/register`
   - Click "Try it out"
   - Fill in:
   ```json
   {
     "email": "test@example.com",
     "username": "testuser",
     "password": "Test123456",
     "full_name": "Test User"
   }
   ```
   - Click "Execute"
   - Should return 201 Created

✅ **Checkpoint 1**: Backend is running, database connected, user registration works!

---

## 🎨 Part 2: Frontend Setup (Week 1, Day 2-3)

### Step 1: Initialize React Project (15 min)

```bash
# Navigate to project root
cd ..  # Should be in trading_resources/

# Create React app with Vite
npm create vite@latest frontend -- --template react-ts

# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Install additional packages
npm install @mui/material @emotion/react @emotion/styled
npm install @tanstack/react-query axios react-router-dom
npm install recharts date-fns
```

### Step 2: Configure API Connection (10 min)

Create `.env` file in `frontend/`:
```bash
VITE_API_URL=http://localhost:8000
```

Create API client (`frontend/src/services/api.ts`):
```typescript
import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default api;
```

### Step 3: Create Basic Pages (20 min)

**Login Page** (`frontend/src/pages/Login.tsx`):
```typescript
import { useState } from 'react';
import api from '../services/api';

export default function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await api.post('/api/v1/auth/login', {
        username_or_email: email,
        password: password,
      });
      localStorage.setItem('access_token', response.data.access_token);
      window.location.href = '/dashboard';
    } catch (error) {
      console.error('Login failed:', error);
      alert('Login failed');
    }
  };

  return (
    <form onSubmit={handleLogin}>
      <h1>Login</h1>
      <input
        type="email"
        placeholder="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />
      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      <button type="submit">Login</button>
    </form>
  );
}
```

### Step 4: Run Frontend (5 min)

```bash
# Start development server
npm run dev

# Should start on http://localhost:5173
```

✅ **Checkpoint 2**: Frontend running, can make API calls to backend!

---

## 🔐 Part 3: 2FA Setup (Week 1, Day 6)

### Step 1: Setup 2FA Endpoint (Backend)

Already implemented in `backend/app/api/v1/auth.py`!

### Step 2: Test 2FA Flow

1. **Register new user** (via Swagger UI or frontend)

2. **Login to get access token**

3. **Setup 2FA**:
   ```bash
   curl -X GET http://localhost:8000/api/v1/auth/2fa/setup \
     -H "Authorization: Bearer <your-access-token>"
   ```

4. **Scan QR code** with Google Authenticator app

5. **Enter 6-digit code** to verify

✅ **Checkpoint 3**: 2FA working end-to-end!

---

## 🚀 Part 4: Deployment (Week 2+)

### Backend Deployment (Railway)

1. **Push code to GitHub**
   ```bash
   git add .
   git commit -m "Backend ready for deployment"
   git push
   ```

2. **Create Railway Project**
   - Go to [railway.app](https://railway.app)
   - "New Project" → "Deploy from GitHub repo"
   - Select your repository
   - Railway auto-detects Python

3. **Add Environment Variables**
   - Go to project → Variables
   - Add all variables from `.env`
   - Set `PORT=8000`

4. **Deploy**
   - Railway automatically deploys
   - Get public URL: `https://your-app.railway.app`

### Frontend Deployment (Vercel)

1. **Update API URL**
   ```bash
   # frontend/.env.production
   VITE_API_URL=https://your-app.railway.app
   ```

2. **Deploy to Vercel**
   - Go to [vercel.com](https://vercel.com)
   - "New Project" → Import Git Repository
   - Select your repository
   - Root Directory: `frontend`
   - Framework: Vite
   - Click "Deploy"

3. **Update CORS**
   ```bash
   # backend/.env
   BACKEND_CORS_ORIGINS=https://your-app.vercel.app
   ```

✅ **Checkpoint 4**: App deployed and accessible online!

---

## 🐛 Troubleshooting

### Backend Won't Start

**Error**: `ModuleNotFoundError: No module named 'fastapi'`
```bash
# Solution: Activate virtual environment
source tradingEnv/bin/activate
pip install -r requirements.txt
```

**Error**: `Could not connect to database`
```bash
# Solution: Check DATABASE_URL in .env
# Make sure Supabase database is running
# Test connection with psql
```

### Frontend Can't Connect to Backend

**Error**: `Network Error` or `CORS error`
```bash
# Solution 1: Check backend is running on port 8000
# Solution 2: Check CORS origins in backend/.env
# BACKEND_CORS_ORIGINS=http://localhost:5173
```

### 2FA QR Code Not Working

**Error**: QR code doesn't scan
```bash
# Solution: Make sure you're using correct TOTP app
# Google Authenticator, Authy, or Microsoft Authenticator
# Try generating new QR code
```

---

## 📚 Next Steps

After completing setup:

1. **Week 1**: Complete authentication + 2FA (Days 1-7)
2. **Week 2**: Add stock search and analysis endpoints
3. **Week 3**: Build portfolio management features
4. **Week 4**: Create frontend dashboard and charts

## 🆘 Getting Help

- Check logs: `backend/logs/app.log`
- API docs: http://localhost:8000/docs
- GitHub Issues: Create issue with error details

---

**Setup Time Checklist:**
- [ ] Backend running (30 min)
- [ ] Database connected (20 min)
- [ ] User registration works (10 min)
- [ ] Frontend running (20 min)
- [ ] API calls working (10 min)
- [ ] 2FA setup (30 min)

**Total: ~2 hours for MVP!**
