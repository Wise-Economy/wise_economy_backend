from django.http import JsonResponse
import json
from app_backend.helpers.user_connection_helper import update_saltedge_connection_success
from django.contrib import auth
from app_backend.models.user import USER_DEFAULTS
from django.http import HttpResponseForbidden


def connection_success(request):
    # this will be called by frontend app after successful saltedge connect session url_redirect to
    # <domain_url>/connection_success?connection_id=salt_edge_connection_id in the app.
    # The app should capture the se_connection_id from the url redirect
    # and send this id along with user_connection_id(our internal id for connections)
    # to this endpoint.
    user = request.user
    if user is not None:
        auth.authenticate(
            request=request,
            username=user.email,
            password=USER_DEFAULTS.DEFAULT_PASSWORD,
        )
        if user.is_authenticated:
            body = json.loads(request.body)
            if update_saltedge_connection_success(
                se_connection_id=body['se_connection_id'],
                user_connection_id=body['user_connection_id'],
            ):
                return JsonResponse({"success": True})
        else:
            return HttpResponseForbidden(content=json.dumps({"message": "INVALID_SESSION"}))

