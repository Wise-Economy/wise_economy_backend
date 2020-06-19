from django.http import JsonResponse
from app_backend.models.user import AppUser
from django.http import HttpResponseForbidden, HttpResponseServerError
from app_backend.models.country import Country
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def get_countries_linkable_for_homescreen(request):
    user = request.user
    if user.is_authenticated:
        app_user = AppUser.get_by_user(user)
        india = Country.objects.get(se_country_code='IN')
        countries_linkable = [
            {
                "country_id": app_user.resident_country.id,
                "country_name": app_user.resident_country.country_name,
            },
            {
                "country_id": india.id,
                "country_name": india.country_name,
            },
        ]
        return JsonResponse({
            "countries_linkable": countries_linkable,
        })
    else:
        return HttpResponseForbidden
