from django.http import HttpResponse


def event(request, request_fields):
    return HttpResponse(status=200)
