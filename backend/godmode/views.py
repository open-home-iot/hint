from rest_framework import views, status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from backend.broker import producer
from backend.user.permissions import IsSuperUser
from backend.home.models import Home
from backend.home.serializers import HomeSerializer
from backend.hume.models import Hume
from backend.hume.serializers import HumeSerializer


class Homes(views.APIView, LimitOffsetPagination):
    """Allows superusers access to list HOMEs."""

    permission_classes = [IsAuthenticated, IsSuperUser]

    # DON'T REMOVE, EVERYTHING BREAKS :((((
    default_limit = 5

    def get(self, request):
        """
        Procure potential homes to latency test.

        Applies 'limit' and 'offset' query parameters to the result set by
        default and returns links for both previous and next pages in the
        response body.
        """
        homes = Home.objects.all()
        queryset = self.paginate_queryset(homes, request)
        return self.get_paginated_response(
            HomeSerializer(queryset, many=True).data
        )


class Humes(views.APIView):

    permission_classes = [IsAuthenticated, IsSuperUser]

    @staticmethod
    def get(request, home_id: int):
        """Get all humes related to a home."""
        queryset = Hume.objects.filter(home__id=home_id)
        return Response(data=HumeSerializer(queryset, many=True).data)


class LatencyTest(views.APIView):
    """Allows Humes to get central broker authentication details."""

    permission_classes = [IsAuthenticated, IsSuperUser]

    @staticmethod
    def get(request):
        """
        Start a latency test for the given HOME.
        """
        humes = request.query_params.get("humes")
        if humes is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        for hume in humes.split(","):
            producer.latency_test(hume)

        return Response(status=status.HTTP_200_OK)
