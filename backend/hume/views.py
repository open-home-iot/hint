from django.http import HttpResponse


def attach(request, request_fields):
    return HttpResponse(status=200)


def authentication(request, request_fields):
    return HttpResponse(status=200)


def token_update(request, request_fields):
    return HttpResponse(status=200)
