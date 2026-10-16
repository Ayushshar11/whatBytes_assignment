
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    EmailLoginView,
    current_user,
    health_check,
    register_user,
)

urlpatterns = [
    path("register/", register_user, name="register"),
    path("login/", EmailLoginView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("me/", current_user, name="current-user"),
    path("health/", health_check, name="health-check"),
]
