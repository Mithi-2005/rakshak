"""Claim routes."""

from django.http import HttpRequest, JsonResponse
from django.urls import path
from django.views.decorators.http import require_GET

from accounts.core.dependencies import get_current_user
from accounts.core.http import api_handler
from accounts.db.session import get_db_session
from claims.schemas.claim import ClaimOut
from claims.services.claim_service import list_user_claims


@require_GET
@api_handler
def list_claims(request: HttpRequest) -> JsonResponse:
    with get_db_session() as db:
        user = get_current_user(request, db)
        claims = [
            ClaimOut.model_validate(item).model_dump(mode="json")
            for item in list_user_claims(user.id, db)
        ]
    return JsonResponse({"items": claims}, status=200)


urlpatterns = [
    path("", list_claims, name="claim-list"),
]

