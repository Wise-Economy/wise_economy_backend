from django.urls import path
from app_backend.views import health, user
from app_backend.views import saltedge_callbacks

urlpatterns = [
    path('health', health.health, name='health',),
    path('users/google_connect', user.google_connect, name='google_connect',),
    path('users/register', user.register, name='user_register',),
    path('users/logout', user.logout_view, name='user_logout_view', ),
    path(
        'users/get_enabled_countries',
        user.get_enabled_countries,
        name='user_get_enabled_countries',
    ),
    path(
        'saltedge/callbacks/connection_success',
        saltedge_callbacks.connection_success,
        name='saltedge_conn_success',
    ),
]

