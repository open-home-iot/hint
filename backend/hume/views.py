from rest_framework import views
from rest_framework.response import Response
from rest_framework import status

from .models import Hume
from .serializers import HumeSerializer


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
                    status=status.HTTP_409_CONFLICT)

        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)
