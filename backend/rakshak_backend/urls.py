"""rakshak_backend URL Configuration"""

from django.urls import path, include

urlpatterns = [
    path("auth/", include("accounts.routes.auth")),
    path("user/", include("accounts.routes.user")),
]
