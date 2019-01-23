from django.http import HttpResponse


def event(request, request_fields=None):
    return HttpResponse(status=200)
