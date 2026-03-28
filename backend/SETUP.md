# Django Authentication Setup Guide

## Installation & Setup

### 1. Create Virtual Environment
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run Migrations
```bash
python manage.py migrate
```

### 4. Create Superuser (Optional - for admin access)
```bash
python manage.py createsuperuser
```

### 5. Run Development Server
```bash
python manage.py runserver
```

Server runs at: `http://localhost:8000`

---

## API Endpoints

### 1. Sign Up
**POST** `/api/auth/signup/`

Request Body:
```json
{
  "username": "testuser",
  "email": "test@example.com",
  "password": "password123",
  "password2": "password123",
  "first_name": "Test",
  "last_name": "User"
}
```

Response (201):
```json
{
  "message": "User created successfully",
  "user": {
    "id": 1,
    "username": "testuser",
    "email": "test@example.com",
    "first_name": "Test",
    "last_name": "User"
  }
}
```

---

### 2. Login
**POST** `/api/auth/login/`

Request Body:
```json
{
  "username": "testuser",
  "password": "password123"
}
```

Response (200):
```json
{
  "message": "Login successful",
  "user": {
    "id": 1,
    "username": "testuser",
    "email": "test@example.com",
    "first_name": "Test",
    "last_name": "User"
  }
}
```

---

### 3. Get Current User
**GET** `/api/auth/user/` (Requires Authentication)

Headers:
```
Cookie: sessionid=<session_id>
```

Response (200):
```json
{
  "id": 1,
  "username": "testuser",
  "email": "test@example.com",
  "first_name": "Test",
  "last_name": "User"
}
```

---

### 4. Logout
**POST** `/api/auth/logout/` (Requires Authentication)

Response (200):
```json
{
  "message": "Logout successful"
}
```

---

## Testing with cURL

```bash
# Sign Up
curl -X POST http://localhost:8000/api/auth/signup/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123",
    "password2": "password123",
    "first_name": "Test",
    "last_name": "User"
  }'

# Login
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -c cookies.txt \
  -d '{
    "username": "testuser",
    "password": "password123"
  }'

# Get Current User (using saved cookies)
curl -X GET http://localhost:8000/api/auth/user/ \
  -b cookies.txt

# Logout
curl -X POST http://localhost:8000/api/auth/logout/ \
  -b cookies.txt
```

---

## Testing with Postman

1. **Sign Up**: POST `http://localhost:8000/api/auth/signup/`
2. **Login**: POST `http://localhost:8000/api/auth/login/`
   - Enable "Automatically follow redirects" if needed
3. **Get User**: GET `http://localhost:8000/api/auth/user/`
4. **Logout**: POST `http://localhost:8000/api/auth/logout/`

---

## File Structure
```
backend/
├── manage.py
├── requirements.txt
├── SETUP.md
├── db.sqlite3
├── rakshak_backend/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── accounts/
    ├── migrations/
    ├── __init__.py
    ├── models.py
    ├── serializers.py
    ├── views.py
    ├── urls.py
    ├── apps.py
    └── admin.py
```

---

## Notes

- This uses **Django Session Authentication** (simple for testing)
- Database: SQLite (automatically created)
- All endpoints are fully functional for basic auth testing
- Change `SECRET_KEY` in settings.py before production
