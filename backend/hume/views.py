import uuid

from django.core.exceptions import ValidationError

from rest_framework import views
from rest_framework.response import Response
from rest_framework import status

from .models import Hume, ValidHume
from .serializers import HumeSerializer
from backend.home.models import Home
from backend.user.models import User


class Humes(views.APIView):
    permission_classes = []

    def post(self, request, format=None):
        """
        ! CSRF NOTICE !
        CSRF EXEMPT DUE TO THAT THIS VIEW IS NOT USED BY USERS. CSRF IS NOT
        CHECKED DUE TO NO PERMISSION_CLASSES (NOT CHECKED WHEN
        UNAUTHENTICATED).

        If the HUME does not exist:
        - Create a new HUME

        Else:
        - Invalid request!
        """
        serializer = HumeSerializer(data=request.data)

        if serializer.is_valid():
            hume_uuid = serializer.validated_data["uuid"]

            try:
                ValidHume.objects.get(uuid=hume_uuid)
            except ValidHume.DoesNotExist:
                return Response(status=status.HTTP_403_FORBIDDEN)

            generated_password = str(uuid.uuid1())
            hume_user = User.objects.create_user(
                email=f"{str(hume_uuid).replace('-', '')}@fake.com",
                password=generated_password
            )

            hume = serializer.save()
            hume.hume_user = hume_user
            hume.save()
            return_data = HumeSerializer(hume).data
            return_data.update({
                "hume_user": {
                    "username": hume_user.email,
                    "password": generated_password
                }
            })
            return Response(return_data,
                            status=status.HTTP_201_CREATED)

        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)


class HumeFind(views.APIView):

    def get(self, request, hume_uuid, format=None):
        """
        Get an unpaired HUME, this API is only intended for fetching unpaired
        HUMEs for pairing them with a given HOME instance.
        """
        try:
            hume = Hume.objects.get(uuid=hume_uuid,
                                    home=None)

        # ValidationError is raised if invalid UUID, DoesNotExist happens if
        # the HUME is already associated with a HOME instance.
        except (ValidationError, Hume.DoesNotExist):
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = HumeSerializer(hume)
        return Response(serializer.data, status=status.HTTP_200_OK)


class HumeConfirmPairing(views.APIView):

    def post(self, request, hume_uuid, format=None):
        """
        Pairs the HUME with a HOME instance.
        """
        home_id = request.data["home_id"]

        try:
            hume = Hume.objects.get(uuid=hume_uuid,
                                    home=None)
        except Hume.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            home = Home.objects.get(id=home_id,
                                    users__id=request.user.id)
        except Home.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        hume.home = home
        hume.save()

        return Response(status=status.HTTP_200_OK)


class HomeHumes(views.APIView):

    def get(self, request, home_id, format=None):
        """
        Get all HUME instances for a given HOME.
        """
        # Ensures only objects the current user is allowed to view is returned
        # through the home__users__id filter. It ensures that the HOME instance
        # is owned by the current user.
        humes = Hume.objects.filter(home__id=home_id,
                                    home__users__id=request.user.id)

        if humes:
            serializer = HumeSerializer(humes, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response([], status=status.HTTP_200_OK)
