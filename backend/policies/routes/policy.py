"""Policy API routes."""

from django.http import HttpRequest, JsonResponse
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

from accounts.core.dependencies import get_current_user
from accounts.core.http import api_handler, parse_json_body
from accounts.db.session import get_db_session
from policies.schemas.policy import (
    PolicyDashboardResponse,
    PolicyOut,
    PolicyPurchaseRequest,
)
from policies.services.policy_service import (
    get_dashboard_payload,
    get_prediction_for_user,
    list_user_policies,
    purchase_policy,
)


@require_GET
@api_handler
def plans(request: HttpRequest) -> JsonResponse:
    with get_db_session() as db:
        user = get_current_user(request, db)
        payload = get_prediction_for_user(user, db)
    return JsonResponse(payload, status=200)


@csrf_exempt
@require_POST
@api_handler
def create_policy(request: HttpRequest) -> JsonResponse:
    payload = PolicyPurchaseRequest.model_validate(parse_json_body(request))
    with get_db_session() as db:
        user = get_current_user(request, db)
        policy = purchase_policy(
            user=user,
            plan_id=payload.plan_id,
            coverage_amount=payload.coverage_amount,
            premium_amount=payload.premium_amount,
            duration_days=payload.duration_days,
            db=db,
        )
        response = PolicyOut.model_validate(policy)
    return JsonResponse(response.model_dump(mode="json"), status=201)


@require_GET
@api_handler
def list_policies(request: HttpRequest) -> JsonResponse:
    with get_db_session() as db:
        user = get_current_user(request, db)
        policies = [
            PolicyOut.model_validate(item).model_dump(mode="json")
            for item in list_user_policies(user.id, db)
        ]
    return JsonResponse({"items": policies}, status=200)


@require_GET
@api_handler
def dashboard(request: HttpRequest) -> JsonResponse:
    with get_db_session() as db:
        user = get_current_user(request, db)
        payload = get_dashboard_payload(user, db)
        response = PolicyDashboardResponse.model_validate(payload)
    return JsonResponse(response.model_dump(mode="json"), status=200)


urlpatterns = [
    path("plans", plans, name="policy-plans"),
    path("", create_policy, name="policy-create"),
    path("list", list_policies, name="policy-list"),
    path("dashboard", dashboard, name="policy-dashboard"),
]
