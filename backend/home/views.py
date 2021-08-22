from rest_framework import views
from rest_framework.response import Response
from rest_framework import status

from backend.home.serializers import HomeSerializer, RoomSerializer
from backend.home.models import Room, Home


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


class HomeRooms(views.APIView):
    """Exposes Room fetching/creation"""

    @staticmethod
    def get(request, home_id):
        """
        Get all rooms related to a home_id.
        """
        # TODO restrict access to homes that do not belong to the current user
        rooms = Room.objects.filter(home=home_id,
                                    home__users__id=request.user.id)
        serializer = RoomSerializer(rooms, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def post(request, home_id):
        """
        Create a new room for a home.
        """
        if Home.objects.filter(id=home_id,
                               users__id=request.user.id).exists():
            data_dict = {
                "home": home_id,
                "name": request.data["name"]
            }
            serializer = RoomSerializer(data=data_dict)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)

            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "That home does not exist."},
                            status=status.HTTP_404_NOT_FOUND)
