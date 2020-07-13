from django.http import JsonResponse
from app_backend.models.user import AppUser
from django.http import HttpResponseForbidden, HttpResponseServerError
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib import auth
from app_backend.models.user import USER_DEFAULTS
from app_backend.helpers.account_helper import get_countries_accounts_data


@csrf_exempt
def get_countries_linkable_for_homescreen(request):
    user = request.user
    auth.authenticate(
        request=request,
        username=user.email,
        password=USER_DEFAULTS.DEFAULT_PASSWORD,
    )
    if user.is_authenticated:
        app_user = AppUser.get_by_user(user)
        countries_linkable = get_countries_accounts_data(app_user)
        return JsonResponse({
            "countries_linkable": countries_linkable,
        })
    else:
        return HttpResponseForbidden(content=json.dumps({"message": "INVALID_SESSION"}))


