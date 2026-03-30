# Backend Setup (Django + SQLAlchemy + JWT)

## 1. Create and Activate Virtual Environment

```bash
python -m venv venv
# Windows
venv\Scripts\activate
```

## 2. Install Dependencies

```bash
pip install -r requirements.txt
```

## 3. Configure Environment Variables

```bash
# PostgreSQL
set DB_NAME=rakshak_db
set DB_USER=postgres
set DB_PASSWORD=your_password
set DB_HOST=localhost
set DB_PORT=5432

# JWT
set JWT_SECRET_KEY=change-this-in-production
set JWT_ALGORITHM=HS256
set ACCESS_TOKEN_EXPIRE_MINUTES=1440
```

You can also use a single connection string:

```bash
set DATABASE_URL=postgresql+psycopg://postgres:your_password@localhost:5432/rakshak_db
```

## 4. Run Server

```bash
python manage.py runserver
```

SQLAlchemy tables are initialized automatically on app startup.

## 5. API Endpoints

### Signup

POST /auth/signup

```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "strongpassword"
}
```

### Login

POST /auth/login

```json
{
  "email": "john@example.com",
  "password": "strongpassword"
}
```

### Current User

GET /auth/me

Header:

Authorization: Bearer <token>

### Create/Update Profile

POST /user/profile

Header:

Authorization: Bearer <token>

```json
{
  "phone": "9876543210",
  "platform": "BikeTaxi",
  "city": "Bengaluru",
  "vehicle_type": "Bike",
  "avg_daily_income": 1400.0
}
```

### Get Profile

GET /user/profile

Header:

Authorization: Bearer <token>

## 6. Authorization Rules

- Default role is always USER on signup.
- ADMIN role is reserved and can be checked through reusable authorization dependency.
- JWT payload includes user_id and role.
