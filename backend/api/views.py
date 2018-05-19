import json
import os
from datetime import datetime

from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie

from rest_framework import viewsets, pagination, permissions, status
from rest_framework.views import APIView

from backend import settings
from api.pagination import PaginationMixin

from api.models import Info
from api.serializer import *

from surveillance.models import AlarmHistory


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    pagination_class = pagination.LimitOffsetPagination
    permission_classes = (permissions.IsAuthenticated, )


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    pagination_class = pagination.LimitOffsetPagination
    permission_classes = (permissions.IsAuthenticated, )


class InfoViewSet(viewsets.ModelViewSet):
    queryset = Info.objects.all()
    serializer_class = InfoSerializer
    pagination_class = pagination.LimitOffsetPagination
    permission_classes = (permissions.BasePermission, )  # Able to view without auth.


class PictureList(APIView, PaginationMixin):

    def get(self, request, format=None):
        year = request.query_params.get('year', None)
        month = request.query_params.get('month', None)

        base_search_dir = '{}{}'.format(settings.STATIC_ROOT, '/alarm_pictures/')

        if year and month:
            search_dir = '{}{}/'.format(base_search_dir,
                                        str(year) + '_' + str(month))
        else:
            search_dir = '{}{}/'.format(base_search_dir,
                                        datetime.now().strftime('%Y_%m'))

        if os.path.exists(search_dir):
            results = os.listdir(search_dir)
        else:
            results = []

        # Set iterates over the result set, but on a C level which makes it a hell of a lot faster.
        sorted_results = sorted(set(results))

        return self.paginate_response(sorted_results, request)


class AlarmHistoryList(viewsets.ModelViewSet):
    serializer_class = AlarmHistorySerializer
    pagination_class = pagination.LimitOffsetPagination
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):

        year = self.request.query_params.get('year', None)
        month = self.request.query_params.get('month', None)

        if year and month:
            queryset = AlarmHistory.objects.filter(date__year=year, date__month=month)
        else:
            now = datetime.now()
            queryset = AlarmHistory.objects.filter(date__year=now.year, date__month=now.month)

        return queryset


@csrf_exempt
@ensure_csrf_cookie
def get_csrf_token(request):
    return HttpResponse(status=status.HTTP_200_OK)


def login_user(request):
    if request.user.is_authenticated:
        return HttpResponse(status=status.HTTP_200_OK)

    request_body = request.body.decode('utf-8')
    dict_request_body = json.loads(request_body)
    username = dict_request_body['username']
    password = dict_request_body['password']

    user = authenticate(username=username, password=password)

    if user is not None:
        login(request, user)
        return HttpResponse(status=status.HTTP_200_OK)
    else:
        response = HttpResponse(status=status.HTTP_401_UNAUTHORIZED)
        response['WWW-Authenticate'] = 'Invalid username or password'
        return response


def logout_user(request):
    logout(request)
    return HttpResponse(status=status.HTTP_200_OK)
