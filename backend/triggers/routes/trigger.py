"""Trigger inspection routes."""

from django.http import HttpRequest, JsonResponse
from django.urls import path
from django.views.decorators.http import require_GET
from sqlalchemy import select

from accounts.core.dependencies import get_current_user
from accounts.core.http import api_handler
from accounts.db.session import get_db_session
from accounts.models import UserProfile
from triggers.schemas.trigger import TriggerEventOut
from triggers.services.event_service import list_trigger_events


@require_GET
@api_handler
def trigger_events(request: HttpRequest) -> JsonResponse:
    with get_db_session() as db:
        user = get_current_user(request, db)
        profile = db.scalar(select(UserProfile).where(UserProfile.user_id == user.id))
        pincode = request.GET.get("pincode") or (profile.pincode if profile else None)
        items = [
            TriggerEventOut.model_validate(item).model_dump(mode="json")
            for item in list_trigger_events(db, pincode=pincode)
        ]
    return JsonResponse({"items": items}, status=200)


urlpatterns = [
    path("events", trigger_events, name="trigger-events"),
]

