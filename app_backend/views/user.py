from django.http import JsonResponse
from app_backend.models.user import AppUser
from django.views.decorators.csrf import csrf_exempt
from django.contrib import auth
import json
from datetime import datetime


@csrf_exempt
def register(request):
    user_payload = json.loads(request.body)
    AppUser.objects.create_user(
        username=user_payload['username'],
        email=user_payload['email'],
        password=user_payload['password'],
    )
    return login(request)


@csrf_exempt
def login(request):
    login_payload = json.loads(request.body)
    app_user = auth.authenticate(
        username=login_payload['username'],
        password=login_payload['password']
    )
    if app_user is not None and app_user.is_active:
        auth.login(request, app_user)
        return JsonResponse({"success": True, "session": request.session.session_key})
