from django.http import JsonResponse
from app_backend.models.users import User
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def register(request):

    new_user = User.objects.create_user(
        username='bla',
        email='asdf@mac.com',
        password="asdfdsfasdf"
    )