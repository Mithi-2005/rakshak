"""Reusable auth dependencies for protected routes."""

from django.http import HttpRequest
from sqlalchemy import select
from sqlalchemy.orm import Session

import jwt

from accounts.core.exceptions import APIError
from accounts.core.security import decode_access_token
from accounts.models import User, UserRole


def _extract_bearer_token(request: HttpRequest) -> str:
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        raise APIError(401, "Missing or invalid Authorization header")
    return auth_header.split(" ", 1)[1].strip()


def get_current_user(request: HttpRequest, db: Session) -> User:
    token = _extract_bearer_token(request)
    try:
        payload = decode_access_token(token)
    except jwt.InvalidTokenError as exc:
        raise APIError(401, "Invalid or expired token") from exc

    user_id = payload.get("user_id")
    if user_id is None:
        raise APIError(401, "Token payload missing user_id")

    user = db.scalar(select(User).where(User.id == int(user_id)))
    if user is None or not user.is_active:
        raise APIError(401, "User not found or inactive")

    request.current_user = user
    return user


def require_admin(user: User) -> None:
    if user.role != UserRole.ADMIN:
        raise APIError(403, "Admin access required")
