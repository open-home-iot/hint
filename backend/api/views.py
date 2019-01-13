from django.http import HttpResponse


def heartbeat(request, request_fields):
    return HttpResponse(status=200)
