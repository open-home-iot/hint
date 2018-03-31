from django.contrib.auth.models import User, Group

from rest_framework import viewsets, pagination

from api.models import Info
from api.serializer import UserSerializer, GroupSerializer, InfoSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    pagination_class = pagination.LimitOffsetPagination
# To specify specific permission and authentication classes for different
# viewsets, uncomment the lines below and add the appropriate imports.
#    permission_classes = (IsAdminUser, )
#    authentication_classes = (BasicAuthentication, )


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    pagination_class = pagination.LimitOffsetPagination


class InfoViewSet(viewsets.ModelViewSet):
    queryset = Info.objects.all()
    serializer_class = InfoSerializer
    pagination_class = pagination.LimitOffsetPagination
