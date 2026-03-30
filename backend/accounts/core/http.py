"""HTTP utility helpers for route handlers."""

import json
from functools import wraps
from typing import Any, Callable

from django.http import HttpRequest, JsonResponse
from pydantic import ValidationError

from accounts.core.exceptions import APIError


def parse_json_body(request: HttpRequest) -> dict[str, Any]:
    if not request.body:
        return {}
    try:
        return json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError as exc:
        raise APIError(400, "Invalid JSON body") from exc


def api_handler(view_func: Callable[..., JsonResponse]) -> Callable[..., JsonResponse]:
    @wraps(view_func)
    def wrapper(*args: Any, **kwargs: Any) -> JsonResponse:
        try:
            return view_func(*args, **kwargs)
        except ValidationError as exc:
            return JsonResponse(
                {"detail": "Validation error", "errors": exc.errors()}, status=422
            )
        except APIError as exc:
            return JsonResponse({"detail": exc.message}, status=exc.status_code)
        except Exception:
            return JsonResponse({"detail": "Internal server error"}, status=500)

    return wrapper
