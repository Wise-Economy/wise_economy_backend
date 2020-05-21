from django.http import JsonResponse
import json
from app_backend.models.user_connection import UserConnection

def connection_success(request):
    # this will be called by frontend app after successful saltedge connect session url_redirect to
    # <domain_url>/connection_success?connection_id=salt_edge_connection_id in the app.
    # The app should capture the se_connection_id from the url redirect
    # and send this id along with user_connection_id(our internal id for connections)
    # to this endpoint.

    body = json.loads(request.body)
    UserConnection.update_saltedge_connection_success(
        se_connection_id=body['se_connection_id'],
        user_connection_id=body['user_connection_id']
    )
    return JsonResponse({"success": True})
