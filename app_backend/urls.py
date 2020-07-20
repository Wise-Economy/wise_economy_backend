from django.urls import path, re_path
from app_backend.views import health, user
from app_backend.views import saltedge_callbacks
from app_backend.views import saltedge
from app_backend.views import global_home_screen


urlpatterns = [
    path('health', health.health, name='health', ),
    path('users/google_connect', user.google_connect, name='google_connect', ),
    path('users/register', user.register, name='user_register', ),
    path('users/logout', user.logout_view, name='user_logout_view', ),
    re_path(
        r'^saltedge/connect/',
        saltedge.saltedge_connect,
        name="saltedge_saltedge_connect",
    ),
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
    path(
        'saltedge/callbacks/fetch_accounts',
        saltedge_callbacks.fetch_accounts_from_saltedge,
        name='fetch_accounts_from_saltedge',
    ),
    path(
        'global_home_screen/countries_linkable/show',
        global_home_screen.get_countries_linkable_for_homescreen,
        name='global_home_screen_get_countries_linkable_for_homescreen',
    ),
]
