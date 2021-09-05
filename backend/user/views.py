import json

from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework import views
from rest_framework.response import Response
from rest_framework import status

from backend.user.serializers import UserSerializer
from backend.user.models import User


class UserSignup(views.APIView):
    """Allows (human) users to create new user accounts."""

    # Default is IsAuthenticated, but we don't need to be authenticated to
    # create an account.
    permission_classes = []

    @staticmethod
    def post(request):
        """
        Create a new user.
        """
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserSelf(views.APIView):
    """Get or update information about the currently authenticated user."""

    @staticmethod
    def get(request):
        """
        Get request user.
        """
        user = User.objects.get(pk=request.user.id)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def put(request):
        """
        Update a user's information.
        """
        serializer = UserSerializer(request.user,
                                    data=request.data,
                                    partial=True)

        if serializer.is_valid():
            # Don't call save on the serializer! This is just to verify the
            # input data is valid.

            # Now, get the current user instance and update it!
            user = User.objects.get(email=request.user.email)

            if serializer.validated_data.get("email") is not None:
                user.email = serializer.validated_data.pop("email")

            if serializer.validated_data.get("password") is not None:
                user.set_password(serializer.validated_data.pop("password"))

            if serializer.validated_data.get("first_name") is not None:
                user.first_name = serializer.validated_data.pop("first_name")

            if serializer.validated_data.get("last_name") is not None:
                user.last_name = serializer.validated_data.pop("last_name")

            user.save()

            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def login_user(request):
    """
    Log in a user.
    """

    if request.method != 'POST':
        return JsonResponse(
            {'auth': ['Wrong method.']},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

    if request.user.is_authenticated:
        return JsonResponse(
            {'auth': ['Already signed in.']}, status=status.HTTP_200_OK
        )

    request_body = request.body.decode('utf-8')
    dict_request_body = json.loads(request_body)
    username = dict_request_body['username']
    password = dict_request_body['password']

    user = authenticate(username=username, password=password)

    if user is not None:
        login(request, user)
        return JsonResponse({'auth': ['Signed in successfully.']},
                            status=status.HTTP_200_OK)

    response = JsonResponse({'auth': ['Invalid credentials']},
                            status=status.HTTP_401_UNAUTHORIZED)
    response['WWW-Authenticate'] = 'Invalid username or password'
    return response


@csrf_exempt
def logout_user(request):
    """
    Log out a user.
    """

    if request.method == 'POST':
        logout(request)
        return JsonResponse({'auth': ['Signed out successfully.']}, status=200)
    return JsonResponse({'auth': ['Wrong method.']},
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)
