"""Lightweight CORS middleware for local frontend integration."""

from __future__ import annotations

import os

from django.http import HttpResponse


def _get_allowed_origins() -> set[str]:
    raw = os.getenv(
        "CORS_ALLOWED_ORIGINS",
        "http://localhost:3000,http://127.0.0.1:3000,http://localhost:3001,http://127.0.0.1:3001",
    )
    return {item.strip() for item in raw.split(",") if item.strip()}


class SimpleCorsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.allowed_origins = _get_allowed_origins()
        self.allowed_methods = "GET, POST, PUT, PATCH, DELETE, OPTIONS"
        self.allowed_headers = "Authorization, Content-Type"

    def __call__(self, request):
        origin = request.headers.get("Origin", "")

        if request.method == "OPTIONS":
            response = HttpResponse(status=200)
        else:
            response = self.get_response(request)

        if origin in self.allowed_origins:
            response["Access-Control-Allow-Origin"] = origin
            response["Vary"] = "Origin"
            response["Access-Control-Allow-Methods"] = self.allowed_methods
            response["Access-Control-Allow-Headers"] = self.allowed_headers
            response["Access-Control-Allow-Credentials"] = "true"

        return response
