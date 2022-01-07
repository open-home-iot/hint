import uuid

from django.core.exceptions import ValidationError
from django.conf import settings

from rest_framework import views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from backend.hume.models import Hume, ValidHume
from backend.hume.serializers import HumeSerializer

from backend.home.models import Home
from backend.user.models import User

from backend.broker import producer

from backend.user.permissions import IsHume


class Humes(views.APIView):
    """Allows Humes to instantiate themselves with HINT."""

    permission_classes = []  # Implies no CSRF check.

    @staticmethod
    def post(request):
        """
        If the HUME does not exist, and there is a ValidHume record:
        - Create a new HUME

        Elif a HUME already exists:
        - Conflict!

        Else:
        - Invalid request!
        """
        try:
            Hume.objects.get(uuid=request.data["uuid"])
            return Response(status=status.HTTP_409_CONFLICT)
        except Hume.DoesNotExist:
            pass

        serializer = HumeSerializer(data=request.data)

        if serializer.is_valid():
            hume_uuid = serializer.validated_data["uuid"]

            try:
                ValidHume.objects.get(uuid=hume_uuid)
            except ValidHume.DoesNotExist:
                return Response(status=status.HTTP_403_FORBIDDEN)

            generated_password = str(uuid.uuid1())
            hume_user = User.objects.create_hume_user(hume_uuid,
                                                      generated_password)

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


class BrokerCredentials(views.APIView):
    """Allows Humes to get central broker authentication details."""

    permission_classes = [IsAuthenticated, IsHume]

    @staticmethod
    def get(request):
        """
        Get broker credentials for the requesting HUME.
        """
        return Response({"username": settings.HUME_BROKER_USERNAME,
                         "password": settings.HUME_BROKER_PASSWORD},
                        status=status.HTTP_200_OK)


###############################################################################
# AJAX VIEWS
###############################################################################
class HumeSingle(views.APIView):
    """Search endpoint to find an unpaired Hume."""

    @staticmethod
    def get(request, hume_uuid):
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

    @staticmethod
    def patch(request, hume_uuid):
        """
        Change the name of a hume.
        """
        try:
            hume = Hume.objects.get(uuid=hume_uuid,
                                    home__users__id=request.user.id)
        except Hume.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = HumeSerializer(hume, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def delete(request, hume_uuid):
        """
        Delete a hume.
        """
        try:
            hume_to_be_deleted = Hume.objects.get(
                uuid=hume_uuid, home__users__id=request.user.id
            )
            hume_to_be_deleted.delete()
        except Hume.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_200_OK)


class HumeConfirmPairing(views.APIView):
    """Confirm an unpaired hume as paired with a home."""

    @staticmethod
    def post(request, hume_uuid):
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
            return Response(status=status.HTTP_404_NOT_FOUND)

        hume.home = home
        hume.save()

        return Response(status=status.HTTP_200_OK)


class HomeHumes(views.APIView):
    """Get all Humes associated with a home"""

    @staticmethod
    def get(request, home_id):
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


class HumeAttachDevice(views.APIView):
    """Attach a discovered device."""

    @staticmethod
    def post(request, home_id, hume_uuid, identifier):
        """
        Attach the device with the input address to the input HUME.
        """
        try:
            Hume.objects.get(
                uuid=hume_uuid,
                home__id=home_id,
                home__users__id=request.user.id
            )
        except Hume.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        producer.attach(hume_uuid, identifier)

        return Response(status=status.HTTP_200_OK)
