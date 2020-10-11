from rest_framework import views
from rest_framework.response import Response
from rest_framework import status

from .serializers import HomeSerializer


class Homes(views.APIView):

    def get(self, request, format=None):
        """
        Get all HOME instances for the current user.
        """
        homes = request.user.home_set.all()
        serializer = HomeSerializer(homes, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        """
        Create a new HOME instance.
        """
        serializer = HomeSerializer(data=request.data)
        if serializer.is_valid():
            home = serializer.save()
            home.users.add(request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
