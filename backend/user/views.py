from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect

from rest_framework import views
from rest_framework.response import Response
from rest_framework import status

import json

from .serializers import UserSerializer
from .models import User


class Users(views.APIView):
    # Default is IsAuthenticated, but we don't need to be authenticated to
    # create an account.
    permission_classes = []

    @method_decorator(csrf_protect)
    def post(self, request, format=None):
        """
        Create a new user.
        """
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserSelf(views.APIView):

    def get(self, request, format=None):
        """
        Get request user.
        """
        user = User.objects.get(pk=request.user.id)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


def login_user(request):
    """
    Log in a user.
    """

    if request.user.is_authenticated:
        print("User was already authenticated!")
        return HttpResponse(status=200)

    request_body = request.body.decode('utf-8')
    dict_request_body = json.loads(request_body)
    username = dict_request_body['username']
    password = dict_request_body['password']

    user = authenticate(username=username, password=password)

    if user is not None:
        login(request, user)
        return HttpResponse(status=200)
    else:
        response = JsonResponse({'auth': ['Invalid credentials']},
                                status=401)
        response['WWW-Authenticate'] = 'Invalid username or password'
        return response


def logout_user(request):
    """
    Log out a user.
    """
    logout(request)
    return HttpResponse(status=200)
