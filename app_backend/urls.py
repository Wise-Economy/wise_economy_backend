from django.urls import path
from app_backend.views import health


urlpatterns = [
    path('health', health.health, name='health'),
]

