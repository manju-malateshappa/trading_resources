# Testing Guide - Investment Agent Backend

Complete guide for testing the backend API manually and with automated tools.

---

## 🚀 Quick Start Testing

### 1. Start the Backend Server

```bash
cd backend
source venv/bin/activate
python3 -m uvicorn app.main:app --reload
```

Wait for:
```
✓ Investment Agent API v1.0.0 started successfully
INFO:     Uvicorn running on http://127.0.0.1:8000
```

### 2. Open Interactive API Docs

Visit: **http://localhost:8000/docs**

This provides Swagger UI with interactive testing for all endpoints.

---

## 👥 Test Users

Use these pre-created test accounts for testing:

| Email | Username | Password | Purpose |
|-------|----------|----------|---------|
| test3@example.com | testuser3 | Test123456 | General testing |
| alice@test.com | alice | Alice123456 | Multi-user testing |
| bob@test.com | bob | Bob123456 | Multi-user testing |
| charlie@test.com | charlie | Charlie123456 | Multi-user testing |

**Created:** 2025-11-12

---

## 📋 Testing Scenarios

### Scenario 1: User Registration

**Test new user registration:**

1. Open http://localhost:8000/docs
2. Expand `POST /api/v1/auth/register`
3. Click **"Try it out"**
4. Enter test data:

```json
{
  "email": "david@test.com",
  "username": "david",
  "password": "David123456",
  "full_name": "David Smith"
}
```

5. Click **"Execute"**

**Expected Response (201):**
```json
{
  "user_id": "abc-123-def-456",
  "email": "david@test.com",
  "username": "david",
  "message": "Registration successful. Please log in."
}
```

**Test Cases:**

✅ **Valid Registration**
```json
{
  "email": "newuser@test.com",
  "username": "newuser",
  "password": "Test123456",
  "full_name": "New User"
}
```

❌ **Duplicate Email (400 error expected)**
```json
{
  "email": "alice@test.com",
  "username": "alice2",
  "password": "Test123456"
}
```

❌ **Duplicate Username (400 error expected)**
```json
{
  "email": "newuser2@test.com",
  "username": "alice",
  "password": "Test123456"
}
```

❌ **Weak Password (422 validation error expected)**
```json
{
  "email": "test@test.com",
  "username": "test",
  "password": "weak"
}
```

❌ **Invalid Email (422 validation error expected)**
```json
{
  "email": "notanemail",
  "username": "test",
  "password": "Test123456"
}
```

---

### Scenario 2: User Login

**Test successful login:**

1. Open http://localhost:8000/docs
2. Expand `POST /api/v1/auth/login`
3. Click **"Try it out"**
4. Enter credentials:

```json
{
  "username_or_email": "alice",
  "password": "Alice123456"
}
```

5. Click **"Execute"**

**Expected Response (200):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": "abc-123",
    "email": "alice@test.com",
    "username": "alice",
    "full_name": null,
    "is_active": true,
    "is_verified": false,
    "is_2fa_enabled": false
  }
}
```

**Test Cases:**

✅ **Login with Username**
```json
{
  "username_or_email": "alice",
  "password": "Alice123456"
}
```

✅ **Login with Email**
```json
{
  "username_or_email": "alice@test.com",
  "password": "Alice123456"
}
```

❌ **Wrong Password (401 error expected)**
```json
{
  "username_or_email": "alice",
  "password": "WrongPassword"
}
```

❌ **Non-existent User (401 error expected)**
```json
{
  "username_or_email": "nonexistent",
  "password": "Test123456"
}
```

---

### Scenario 3: Protected Endpoints (2FA Setup)

**Test authenticated endpoint access:**

1. **First, login to get access token** (see Scenario 2)

2. **Copy the access_token** from the login response

3. **Expand `GET /api/v1/auth/2fa/setup`**

4. **Click "Try it out"**

5. **Click the 🔒 Authorize button** at the top right

6. **Enter:** `Bearer <your_access_token>`
   - Example: `Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`

7. **Click "Authorize"**, then **"Close"**

8. **Click "Execute"** on the 2FA setup endpoint

**Expected Response (200):**
```json
{
  "secret": "JBSWY3DPEHPK3PXP",
  "qr_code": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA...",
  "backup_codes": [
    "ABCD-1234",
    "EFGH-5678",
    "IJKL-9012",
    "MNOP-3456",
    "QRST-7890"
  ]
}
```

**Test Cases:**

✅ **Valid Token**
- Include valid JWT token in Authorization header

❌ **Missing Token (403 error expected)**
- Don't include Authorization header

❌ **Invalid Token (401 error expected)**
- Include invalid/expired token

❌ **2FA Already Enabled (400 error expected)**
- Try to setup 2FA twice for the same user

---

### Scenario 4: Logout

**Test logout:**

1. **Login and get access token** (see Scenario 2)

2. **Authorize with token** (click 🔒 button)

3. **Expand `POST /api/v1/auth/logout`**

4. **Click "Try it out"** and **"Execute"**

**Expected Response (200):**
```json
{
  "message": "Logged out successfully"
}
```

---

## 🧪 cURL Testing

### Register User
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "curl@test.com",
    "username": "curluser",
    "password": "Curl123456",
    "full_name": "Curl User"
  }'
```

### Login
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username_or_email": "alice",
    "password": "Alice123456"
  }'
```

### 2FA Setup (with token)
```bash
# First, login and get the access token
ACCESS_TOKEN="your_access_token_here"

curl -X GET http://localhost:8000/api/v1/auth/2fa/setup \
  -H "Authorization: Bearer $ACCESS_TOKEN"
```

---

## 🗄️ Database Verification

### View All Users

```bash
cd backend
sqlite3 investment_agent.db "SELECT id, email, username, is_active, is_2fa_enabled, created_at FROM users;"
```

**Current Users:**
```
abc-123-...|test3@example.com|testuser3|1|0|2025-11-12 07:01:43
def-456-...|alice@test.com|alice|1|0|2025-11-12 07:13:07
ghi-789-...|bob@test.com|bob|1|0|2025-11-12 07:13:20
jkl-012-...|charlie@test.com|charlie|1|0|2025-11-12 07:13:31
```

### View User Details

```bash
sqlite3 investment_agent.db "SELECT * FROM users WHERE username='alice';"
```

### View Sessions

```bash
sqlite3 investment_agent.db "SELECT user_id, ip_address, user_agent, is_active, created_at FROM sessions;"
```

### Count Users

```bash
sqlite3 investment_agent.db "SELECT COUNT(*) as total_users FROM users;"
```

### Check Failed Login Attempts

```bash
sqlite3 investment_agent.db "SELECT username, email, failed_login_attempts, locked_until FROM users WHERE failed_login_attempts > 0;"
```

### Clear Database (⚠️ Danger)

```bash
# Delete all users (for testing only!)
sqlite3 investment_agent.db "DELETE FROM users;"

# Verify deletion
sqlite3 investment_agent.db "SELECT COUNT(*) FROM users;"
```

---

## 🐍 Python Testing

### Test with Python Script

Create `test_api.py`:

```python
import requests

BASE_URL = "http://localhost:8000"

# Test registration
def test_register():
    response = requests.post(
        f"{BASE_URL}/api/v1/auth/register",
        json={
            "email": "python@test.com",
            "username": "pythonuser",
            "password": "Python123456",
            "full_name": "Python User"
        }
    )
    print("Register:", response.status_code, response.json())
    return response.json()

# Test login
def test_login(username, password):
    response = requests.post(
        f"{BASE_URL}/api/v1/auth/login",
        json={
            "username_or_email": username,
            "password": password
        }
    )
    print("Login:", response.status_code, response.json())
    return response.json()

# Test 2FA setup
def test_2fa_setup(access_token):
    response = requests.get(
        f"{BASE_URL}/api/v1/auth/2fa/setup",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    print("2FA Setup:", response.status_code, response.json())
    return response.json()

# Run tests
if __name__ == "__main__":
    # Register
    reg_result = test_register()

    # Login
    login_result = test_login("pythonuser", "Python123456")
    access_token = login_result.get("access_token")

    # Setup 2FA
    if access_token:
        test_2fa_setup(access_token)
```

Run:
```bash
python3 test_api.py
```

---

## 🧪 Automated Testing with Pytest

### Install Test Dependencies

```bash
pip install pytest pytest-asyncio httpx
```

### Run Tests

```bash
cd backend
pytest tests/ -v
```

### Test Coverage

```bash
pytest --cov=app tests/
```

---

## 📊 Health Checks

### Server Health

```bash
curl http://localhost:8000/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "database": "connected",
  "version": "1.0.0",
  "environment": "development"
}
```

### Root Endpoint

```bash
curl http://localhost:8000/
```

**Expected Response:**
```json
{
  "name": "Investment Agent API",
  "version": "1.0.0",
  "status": "running",
  "environment": "development",
  "docs": "/docs"
}
```

---

## 🔍 Common Issues & Solutions

### Issue 1: 500 Internal Server Error

**Symptom:** Registration fails with 500 error

**Solution:**
1. Check backend logs for detailed error
2. Verify database connection
3. Restart backend server

### Issue 2: 401 Unauthorized

**Symptom:** Protected endpoints return 401

**Solution:**
1. Verify you're logged in and have access token
2. Check token hasn't expired (30 min expiry)
3. Ensure Authorization header format: `Bearer <token>`

### Issue 3: 422 Validation Error

**Symptom:** Registration/login fails with 422

**Solution:**
1. Check password meets requirements (8+ chars, uppercase, lowercase, digit)
2. Verify email format is valid
3. Username must be 3-50 chars, alphanumeric + underscore/dash

### Issue 4: Database Locked

**Symptom:** SQLite database locked error

**Solution:**
```bash
# Stop backend server
# Delete lock file
rm backend/investment_agent.db-journal

# Restart server
```

---

## 🔐 Security Testing

### Test Account Locking

1. **Try wrong password 5 times** for same user
2. **Expected:** Account locked for 15 minutes
3. **Verify:**
```bash
sqlite3 investment_agent.db "SELECT username, failed_login_attempts, locked_until FROM users WHERE username='testaccount';"
```

### Test JWT Token Expiry

1. **Login and get access token**
2. **Wait 30+ minutes**
3. **Try to access protected endpoint**
4. **Expected:** 401 Unauthorized

### Test Password Strength

Try these and expect validation errors:

- ❌ Too short: `"Test12"`
- ❌ No uppercase: `"test123456"`
- ❌ No lowercase: `"TEST123456"`
- ❌ No digit: `"TestPassword"`
- ✅ Valid: `"Test123456"`

---

## 📝 Test Checklist

Use this checklist to verify all functionality:

### User Registration
- [ ] Register new user successfully
- [ ] Duplicate email rejected (400)
- [ ] Duplicate username rejected (400)
- [ ] Weak password rejected (422)
- [ ] Invalid email rejected (422)
- [ ] User appears in database

### User Login
- [ ] Login with username succeeds
- [ ] Login with email succeeds
- [ ] Wrong password rejected (401)
- [ ] Non-existent user rejected (401)
- [ ] Access token returned
- [ ] Refresh token returned
- [ ] User object returned

### Protected Endpoints
- [ ] 2FA setup requires authentication
- [ ] Valid token allows access
- [ ] Missing token rejected (403)
- [ ] Invalid token rejected (401)
- [ ] QR code generated correctly
- [ ] Backup codes generated

### Session Management
- [ ] Sessions created on login
- [ ] Sessions stored in database
- [ ] Logout invalidates session
- [ ] Multiple sessions supported

### Security
- [ ] Passwords are hashed in database
- [ ] JWT tokens expire correctly
- [ ] Account locking after failed attempts
- [ ] CORS configured correctly

---

## 🎯 Next Steps

Once basic authentication is tested:

1. **Test 2FA Flow**
   - Enable 2FA for a user
   - Login with 2FA code
   - Test backup codes

2. **Test Stock Endpoints** (when implemented)
   - Search stocks
   - Analyze stocks
   - Get stock data

3. **Test Portfolio Endpoints** (when implemented)
   - Create portfolio
   - Add positions
   - Execute trades
   - View performance

---

## 📚 Additional Resources

- **API Documentation:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
- **Architecture:** [docs/ARCHITECTURE.md](./ARCHITECTURE.md)
- **Setup Guide:** [docs/SETUP_GUIDE.md](./SETUP_GUIDE.md)

---

**Last Updated:** 2025-11-12
**Backend Version:** 1.0.0
**Test Users Created:** 2025-11-12
