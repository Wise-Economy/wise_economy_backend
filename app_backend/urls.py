from django.urls import path
from app_backend.views import health, user


urlpatterns = [
    path('health', health.health, name='health'),
    path('users/register', user.register, name='user_registration')
]

