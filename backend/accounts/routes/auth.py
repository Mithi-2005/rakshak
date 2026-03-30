"""Authentication routes using SQLAlchemy + JWT."""

from datetime import datetime, timezone

from django.http import HttpRequest, JsonResponse
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST
from sqlalchemy import func, select

from accounts.core.dependencies import get_current_user
from accounts.core.exceptions import APIError
from accounts.core.http import api_handler, parse_json_body
from accounts.core.security import create_access_token, hash_password, verify_password
from accounts.db.session import get_db_session
from accounts.models import User, UserRole
from accounts.schemas.auth import (
    AuthResponse,
    LoginRequest,
    MeResponse,
    SignupRequest,
    UserOut,
)


@csrf_exempt
@require_POST
@api_handler
def signup(request: HttpRequest) -> JsonResponse:
    payload = SignupRequest.model_validate(parse_json_body(request))
    normalized_email = payload.email.lower()

    with get_db_session() as db:
        existing = db.scalar(
            select(User).where(func.lower(User.email) == normalized_email)
        )
        if existing is not None:
            raise APIError(409, "Email already registered")

        user = User(
            name=payload.name.strip(),
            email=normalized_email,
            password_hash=hash_password(payload.password),
            role=UserRole.USER,
            is_profile_completed=False,
            is_active=True,
            created_at=datetime.now(timezone.utc),
        )
        db.add(user)
        db.flush()

        response = AuthResponse(
            access_token=create_access_token(user_id=user.id, role=user.role.value),
            user=UserOut.model_validate(user),
        )

    return JsonResponse(response.model_dump(mode="json"), status=201)


@csrf_exempt
@require_POST
@api_handler
def login(request: HttpRequest) -> JsonResponse:
    payload = LoginRequest.model_validate(parse_json_body(request))
    normalized_email = payload.email.lower()

    with get_db_session() as db:
        user = db.scalar(select(User).where(func.lower(User.email) == normalized_email))
        if user is None or not verify_password(payload.password, user.password_hash):
            raise APIError(401, "Invalid email or password")
        if not user.is_active:
            raise APIError(403, "User is inactive")

        response = AuthResponse(
            access_token=create_access_token(user_id=user.id, role=user.role.value),
            user=UserOut.model_validate(user),
        )

    return JsonResponse(response.model_dump(mode="json"), status=200)


@require_GET
@api_handler
def me(request: HttpRequest) -> JsonResponse:
    with get_db_session() as db:
        user = get_current_user(request, db)
        response = MeResponse.model_validate(user)

    return JsonResponse(response.model_dump(mode="json"), status=200)


urlpatterns = [
    path("signup", signup, name="auth-signup"),
    path("login", login, name="auth-login"),
    path("me", me, name="auth-me"),
]
