from django.http import HttpResponse


def attach(request):
    return HttpResponse("<p>ATTACH</p>")
