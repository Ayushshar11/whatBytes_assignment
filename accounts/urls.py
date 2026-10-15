
from django.urls import path
from .views import health_check, register_user

urlpatterns = [
    path('health/', health_check, name='health-check'),
    path('register/', register_user, name='register'),
]
