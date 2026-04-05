# Rakshak Local Run

## Services
- `backend/`: Django host + SQLAlchemy persistence + Celery tasks
- `ai_models/`: FastAPI risk and premium service
- `frontend/`: Next.js worker web app

## Environment
- Copy `backend/.env.example` to `backend/.env`
- Copy `ai_models/.env.example` to `ai_models/.env`
- Copy `frontend/.env.example` to `frontend/.env.local`

## Backend
```powershell
cd backend
pip install -r requirements.txt
python manage.py runserver
```

## Celery Worker
```powershell
cd backend
celery -A rakshak_backend.celery:app worker --pool=solo --loglevel=info
```

## Celery Beat
```powershell
cd backend
celery -A rakshak_backend.celery:app beat --loglevel=info
```

## ML Service
```powershell
cd ai_models
pip install -r requirements.txt
uvicorn main:app --reload --port 8001
```

## Frontend
```powershell
cd frontend
npm install
npm run dev
```

## Expected Flow
1. Sign up in the frontend and save profile with a pincode and daily income.
2. Open `Buy Policy` and purchase one of the ML-generated plans.
3. Let Celery beat poll external APIs every 15 minutes.
4. Inspect `/triggers/events` and `/claims/` through the app or API.
5. Nightly claim generation creates claims for active policies affected by stored trigger events.
