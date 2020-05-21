from django.http import JsonResponse


def connection_success(request):
    connection_id = request.META['QUERY_STRING'].split('=')[1]
    print(connection_id)
    # Put code here to get the exact user connection obj in our db from
    # Saltedge connection id.
    # Put code here to start fetching accounts, transactions for that userconnection obj.
    return JsonResponse({"success": True})
