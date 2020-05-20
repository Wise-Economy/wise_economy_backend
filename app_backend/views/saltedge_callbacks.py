from django.http import JsonResponse


def connection_success(request):
    print(request.body)
    return JsonResponse({"success": True})