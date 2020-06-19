from django.http import JsonResponse
from app_backend.models.user import AppUser
from django.http import HttpResponseForbidden, HttpResponseServerError
from app_backend.models.country import Country
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def saltedge_connect(request):
    # This endpoint will initiate the saltedge connect session.
    country_id = request.GET.get('country_id', None)
    country = Country.objects.get(id=country_id)
    user = request.user
    if user.is_authenticated:
        app_user = AppUser.get_by_user(user)
        if app_user.create_or_return_saltedge_user_record():
            user_connection = app_user.create_user_connection_record()
            connect_session_response = user_connection.generate_saltedge_connect_session(
                country_code=country.se_country_code,
            )
            import ipdb; ipdb.set_trace();
            return JsonResponse({
                'expires_at': connect_session_response['data']['expires_at'],
                'connect_url': connect_session_response['data']['connect_url'],
                'user_connection_id': user_connection.id,
            })
        else:
            # Unable to create customer record in Saltedge.
            return HttpResponseServerError
    else:
        return HttpResponseForbidden
