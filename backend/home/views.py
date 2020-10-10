from rest_framework import generics

from .models import Home
from .serializers import HomeSerializer


class CreateHome(generics.CreateAPIView):
    queryset = Home.objects.all()
    serializer_class = HomeSerializer
    permission_classes = ()


class UpdateHome(generics.UpdateAPIView):
    queryset = Home.objects.all()
    serializer_class = HomeSerializer
    permission_classes = ()


class ListHome(generics.ListAPIView):
    queryset = Home.objects.all()
    serializer_class = HomeSerializer
    permission_classes = ()
