from django.http import JsonResponse
from app_backend.models.user import AppUser
from django.views.decorators.csrf import csrf_exempt
from django.contrib import auth
import json
from app_backend.models.user import USER_DEFAULTS, SIGN_IN_METHODS
from django.core.exceptions import ObjectDoesNotExist
from app_backend.helpers.google_auth_helper import verify_google_token
from django.http import HttpResponseForbidden, HttpResponseServerError
from app_backend.models.country import Country


@csrf_exempt
def google_connect(request):
    payload = json.loads(request.body)
    is_new_user = False

    # TODO: What if the user connected the google account but didn't complete profile.
    if not verify_google_token(
            token=payload['google_secret_token'],
            email=payload['email'],
            google_id=payload['google_id']
    ):
        return HttpResponseForbidden(content=json.dumps({"message": "INVALID_GOOGLE_TOKEN"}))

    try:
        app_user = AppUser.objects.get(email=payload['email'])
    except ObjectDoesNotExist:
        is_new_user = True
        app_user = AppUser.objects.create_user(
            username=payload['email'],
            email=payload['email'],
            password=USER_DEFAULTS.DEFAULT_PASSWORD,
            full_name=payload['full_name'],
            google_id=payload['google_id'],
            profile_photo=payload['profile_photo'],
            sign_in_method=SIGN_IN_METHODS.GOOGLE_SIGN_IN,
        )

    return login(
        request=request,
        is_new_user=is_new_user,
        app_user=app_user,
    )


@csrf_exempt
def register(request):
    user_details_payload = json.loads(request.body)
    user = request.user
    if user is not None:
        auth.authenticate(
            request=request,
            username=user.email,
            password=USER_DEFAULTS.DEFAULT_PASSWORD,
        )
        if user.is_authenticated:
            app_user = AppUser.objects.get(id=user.id)
            if app_user.register_user_details(user_details_payload):
                app_user.create_or_return_saltedge_user_record()
                return JsonResponse({
                    "user_details": app_user.get_user_details(),
                })
            else:
                return HttpResponseServerError(content=json.dumps({"message": "FAILED_UPDATE"}))
    return HttpResponseForbidden(content=json.dumps({"message": "INVALID_SESSION"}))


@csrf_exempt
def logout_view(request):
    auth.logout(request)
    return JsonResponse({
        "success": True,
    })


@csrf_exempt
def get_enabled_countries(request):
    enabled_countries = Country.get_enabled_countries()
    response_array = [
        {"country_id": country.id, "country_name": country.country_name }
        for country in enabled_countries
    ]
    return JsonResponse({"enabled_countries_list": response_array})


def login(request, is_new_user, app_user):
    # TODO: What if somebody steals the session from our app. Is that possible?
    login_payload = json.loads(request.body)
    auth.authenticate(
        username=login_payload['email'],
        password=USER_DEFAULTS.DEFAULT_PASSWORD,
    )
    if app_user is not None and app_user.is_active:
        auth.login(request, app_user)
        return JsonResponse({
            "is_new_user": is_new_user,
            "user_details": app_user.get_user_details(),
        })
