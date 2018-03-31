import json, os

from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, JsonResponse
from django.db.models import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie

from channels.layers import get_channel_layer

from asgiref.sync import async_to_sync

from rest_framework import viewsets, pagination, permissions, status

from api.models import Info
from events.models import EventStatus
from events.events import *
from api.serializer import UserSerializer, GroupSerializer, InfoSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    pagination_class = pagination.LimitOffsetPagination
# To specify specific permission and authentication classes for different
# viewsets, uncomment the lines below and add the appropriate imports.
    permission_classes = (permissions.IsAuthenticated, )
#    authentication_classes = (BasicAuthentication, )


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    pagination_class = pagination.LimitOffsetPagination
    permission_classes = (permissions.IsAuthenticated, )


class InfoViewSet(viewsets.ModelViewSet):
    queryset = Info.objects.all()
    serializer_class = InfoSerializer
    pagination_class = pagination.LimitOffsetPagination


def event_alarm(req, alarm):
    print("Got the following alarm status: ", alarm)
    try:
        event_status = EventStatus.objects.get(pk=1)
        event_status.alarm = alarm == 'on'
        event_status.save()
    except ObjectDoesNotExist:
        EventStatus.objects.create(alarm=alarm == 'on')

    layer = get_channel_layer()
    async_to_sync(layer.group_send)('events', {
        'type': EVENT[PROXIMITY_ALARM],
        'content': alarm
    })
    return HttpResponse()


def get_event_status(req):
    alarm_status = False
    try:
        event_status = EventStatus.objects.get(pk=1)
        alarm_status = event_status.alarm
    except ObjectDoesNotExist:
        pass
    finally:
        return JsonResponse({
            'count': 1,
            'next': 'N/A',
            'previous': 'N/A',
            'results': [alarm_status]
        })


def list_pictures(req):
    user = os.getenv('DJANGO_STATIC_DIR', '~/')
    if user == '~/':
        raise EnvironmentError('You do not seem to have installed the project correctly, environment variable missing.')

    p = os.path.expanduser(user) + '/alarm_pictures/'

    result = os.listdir(p)

    return JsonResponse({'pictures': result})


@csrf_exempt
@ensure_csrf_cookie
def get_csrf_token(request):
    return HttpResponse(status=status.HTTP_200_OK)


def login_user(request):
    if request.user.is_authenticated:
        print("User was already authenticated!")
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
