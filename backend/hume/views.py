from django.core.exceptions import ValidationError

from rest_framework import views
from rest_framework.response import Response
from rest_framework import status

from .models import Hume
from .serializers import HumeSerializer
from backend.home.models import Home


class HumePair(views.APIView):
    permission_classes = []

    def post(self, request, format=None):
        """
        ! CSRF NOTICE !
        CSRF EXEMPT DUE TO THAT THIS VIEW IS NOT USED BY USERS. CSRF IS NOT
        CHECKED DUE TO NO PERMISSION_CLASSES (NOT CHECKED WHEN
        UNAUTHENTICATED).

        One of the following happens depending on:

        If the HUME ID already exists:
        - Return HUME.is_paired

        If the HUME does not exist:
        - Create a new HUME
        """
        serializer = HumeSerializer(data=request.data)
        if serializer.is_valid():

            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        uuid_errors = serializer.errors.get("uuid")
        if uuid_errors:
            if uuid_errors[0].code == "unique":
                hume = Hume.objects.get(uuid=serializer.data["uuid"])
                return Response(
                    {"is_paired": hume.is_paired},
                    status=status.HTTP_409_CONFLICT
                )

        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)


class HumeConfirmPairing(views.APIView):

    def put(self, request, hume_id, format=None):
        """
        Puts the HUME in a PAIRED state.
        """
        hume = Hume.objects.filter(id=hume_id,
                                   home__users__id=request.user.id)

        if hume:
            hume = hume[0]
            hume.is_paired = True
            hume.save()

            return Response(status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)


class HumeFind(views.APIView):

    def get(self, request, format=None):
        """
        Get an unassociated HUME.
        """
        try:
            hume = Hume.objects.filter(uuid=request.GET.get('hume_uuid'),
                                       is_paired=False,
                                       home=None)
        except ValidationError:
            return Response({"hume_uuid": ["Invalid UUID."]},
                            status=status.HTTP_400_BAD_REQUEST)

        if hume:
            hume = hume[0]
            serializer = HumeSerializer(hume)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({"hume_uuid": ["Does not exist."]},
                        status=status.HTTP_404_NOT_FOUND)


class HumeAssociate(views.APIView):

    def post(self, request, hume_id, format=None):
        """
        Put the HUME in an ASSOCIATED state and links it to a user's HOME.
        """
        hume = Hume.objects.get(id=hume_id)

        # hume is already associated, protective measure for this API endpoint.
        # Dissalowed here to explicitly implement moving HUMEs in some other
        # view later, makes it more verbose.
        if hume.home:
            return Response({"hume_id": ["Already associated."]},
                            status.HTTP_400_BAD_REQUEST)

        home = Home.objects.filter(id=request.data["home_id"],
                                   users__id=request.user.id)

        if home:
            hume.home = home[0]  # Still a queryset
            hume.save()
            serializer = HumeSerializer(hume)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({"home_id": ["Does not exist."]},
                        status=status.HTTP_400_BAD_REQUEST)


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
