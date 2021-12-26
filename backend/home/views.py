from rest_framework import views
from rest_framework.response import Response
from rest_framework import status

from backend.home.serializers import HomeSerializer
from backend.home.models import Home
from backend.hume.models import Hume
from backend.broker import producer


###############################################################################
# AJAX VIEWS
###############################################################################
class Homes(views.APIView):
    """Exposes Home fetching/creation."""

    @staticmethod
    def get(request):
        """
        Get all HOME instances for the current user.
        """
        homes = request.user.home_set.all()
        serializer = HomeSerializer(homes, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def post(request):
        """
        Create a new HOME instance.
        """
        serializer = HomeSerializer(data=request.data)
        if serializer.is_valid():
            home = serializer.save()
            home.users.add(request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HomeSingle(views.APIView):
    """Exposes singular Home fetching/deletion."""

    @staticmethod
    def get(request, home_id):
        """
        Get the Home with the input ID.
        """
        try:
            home = request.user.home_set.get(id=home_id)
        except Home.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = HomeSerializer(home)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def patch(request, home_id):
        """
        Change a home.
        """
        try:
            home = request.user.home_set.get(id=home_id)
        except Home.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = HomeSerializer(home, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def delete(request, home_id):
        """
        Delete a home.
        """
        try:
            home_to_be_deleted = request.user.home_set.get(id=home_id)
            home_to_be_deleted.delete()
        except Home.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_200_OK)


class HomeDiscoverDevices(views.APIView):
    """Discover devices nearby a Hume."""

    @staticmethod
    def get(request, home_id):
        """
        Request that HINT tell HUME to discover devices.
        """
        humes = Hume.objects.filter(
            home__id=home_id,
            home__users__id=request.user.id
        )
        if not humes.exists():
            return Response(status=status.HTTP_404_NOT_FOUND)

        for hume in humes:
            producer.discover_devices(str(hume.uuid), "")

        return Response(status=status.HTTP_200_OK)
