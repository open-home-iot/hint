from django.http import HttpResponse


def index(request):
    return HttpResponse("<p>API works</p>")
