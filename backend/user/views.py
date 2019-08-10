from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse

from json import loads


def login_user(request):
    if request.user.is_authenticated:
        print("User was already authenticated!")
        return HttpResponse(status=200)

    request_body = request.body.decode('utf-8')
    dict_request_body = loads(request_body)
    username = dict_request_body['username']
    password = dict_request_body['password']

    user = authenticate(username=username, password=password)

    if user is not None:
        login(request, user)
        return HttpResponse(status=200)
    else:
        response = HttpResponse(status=401)
        response['WWW-Authenticate'] = 'Invalid username or password'
        return response


def logout_user(request):
    logout(request)
    return HttpResponse(status=200)