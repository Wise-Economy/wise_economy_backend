from django.urls import path
from app_backend.views import health, user
from app_backend.views import saltedge

urlpatterns = [
    path('health', health.health, name='health',),
    path('users/register', user.register, name='user_register',),
    path('users/login', user.login, name='user_login',),
    path(
        'saltedge/callbacks/connection_success',
        saltedge.connection_success,
        name='saltedge_conn_success',
    )
]

