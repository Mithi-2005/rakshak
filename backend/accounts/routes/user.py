"""User profile routes with one-to-one profile handling."""

from datetime import datetime, timezone

from django.http import HttpRequest, JsonResponse
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from sqlalchemy import select

from accounts.core.dependencies import get_current_user
from accounts.core.exceptions import APIError
from accounts.core.http import api_handler, parse_json_body
from accounts.db.session import get_db_session
from accounts.models import UserProfile
from accounts.schemas.profile import (
    ProfileResponse,
    ProfileUpsertRequest,
    UserProfileOut,
)


def _upsert_profile(request: HttpRequest) -> JsonResponse:
    payload = ProfileUpsertRequest.model_validate(parse_json_body(request))
    if not payload.pincode:
        raise APIError(422, "pincode is required")

    with get_db_session() as db:
        user = get_current_user(request, db)
        profile = db.scalar(select(UserProfile).where(UserProfile.user_id == user.id))

        now = datetime.now(timezone.utc)
        if profile is None:
            profile = UserProfile(user_id=user.id, created_at=now, updated_at=now)
            db.add(profile)

        profile.phone = payload.phone
        profile.platform = payload.platform
        profile.city = payload.city
        profile.pincode = payload.pincode
        profile.vehicle_type = payload.vehicle_type
        profile.avg_daily_income = payload.avg_daily_income
        profile.updated_at = now

        user.is_profile_completed = True
        db.flush()

        response = ProfileResponse(
            profile_completed=True,
            profile=UserProfileOut.model_validate(profile),
        )

    return JsonResponse(response.model_dump(mode="json"), status=200)


def _get_profile(request: HttpRequest) -> JsonResponse:
    with get_db_session() as db:
        user = get_current_user(request, db)
        profile = db.scalar(select(UserProfile).where(UserProfile.user_id == user.id))

        if profile is None:
            response = ProfileResponse(profile_completed=False, profile=None)
            return JsonResponse(response.model_dump(mode="json"), status=200)

        response = ProfileResponse(
            profile_completed=True,
            profile=UserProfileOut.model_validate(profile),
        )

    return JsonResponse(response.model_dump(mode="json"), status=200)


@csrf_exempt
@require_http_methods(["GET", "POST"])
@api_handler
def profile(request: HttpRequest) -> JsonResponse:
    if request.method == "POST":
        return _upsert_profile(request)
    return _get_profile(request)


urlpatterns = [
    path("profile", profile, name="user-profile"),
]
