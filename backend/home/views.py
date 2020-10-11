from rest_framework import views
from rest_framework.response import Response
from rest_framework import status

from .serializers import HomeSerializer


class Homes(views.APIView):

    def post(self, request, format=None):
        """
        Create a new HOME instance.
        """
        serializer = HomeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
