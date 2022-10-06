import uuid

from django.test import TestCase

from rest_framework.test import APIClient
from rest_framework import status

from unittest.mock import patch

from backend.user.models import User
from backend.home.models import Home

from backend.godmode.views import Homes as GodmodeHomes
from backend.hume.models import Hume


class GodmodeApi(TestCase):

    HOMES_URL = "/api/godmode/homes"
    HUMES_URL = "/api/godmode/homes/{}/humes"
    LATENCY_TEST_URL = "/api/godmode/latency-test"

    @classmethod
    def setUpClass(cls):
        """
        Sets up global user for authentication.
        """
        super().setUpClass()
        User.objects.create_superuser(email="super@t.se", password="pw")
        User.objects.create_user(email="normie@t.se", password="pw")

        for i in range(8):
            home = Home.objects.create(name="home" + str(i))
            hume_uuid = uuid.uuid4()
            user = User.objects.create_user(email=f"{hume_uuid}@bla.se")
            Hume.objects.create(uuid=hume_uuid, home=home, hume_user=user)

    def setUp(self):
        """
        CALLED PER TEST CASE!

        Create shared test case data.
        """
        self.client = APIClient()
        self.client.login(username="super@t.se", password="pw")

    def test_api_get_homes(self):
        """
        Verify that a superuser can get HOMEs through the godmode endpoint for
        homes.
        """
        ret = self.client.get(GodmodeApi.HOMES_URL)

        self.assertEqual(ret.status_code, status.HTTP_200_OK)

    def test_api_get_homes_pagination(self):
        """
        Verify that a superuser can get HOMEs through the godmode endpoint for
        homes.
        """
        ret = self.client.get(GodmodeApi.HOMES_URL)

        self.assertEqual(ret.status_code, status.HTTP_200_OK)
        self.assertEqual(len(ret.data["results"]), GodmodeHomes.default_limit)

    def test_api_get_homes_access(self):
        """Verify that only superusers can access godmode homes."""
        client = APIClient()
        client.login(username="normie@t.se", password="pw")

        ret = client.get(GodmodeApi.HOMES_URL)
        self.assertEqual(ret.status_code, status.HTTP_403_FORBIDDEN)

    def test_api_get_humes(self):
        """Verify that humes can be gotten through the godmode API."""
        homes = Home.objects.all()
        ret = self.client.get(GodmodeApi.HUMES_URL.format(homes[0].id))

        self.assertEqual(ret.status_code, status.HTTP_200_OK)

    def test_api_get_humes_access(self):
        """Verify that only superusers can access godmode humes."""
        client = APIClient()
        client.login(username="normie@t.se", password="pw")

        homes = Home.objects.all()
        ret = client.get(GodmodeApi.HUMES_URL.format(homes[0].id))

        self.assertEqual(ret.status_code, status.HTTP_403_FORBIDDEN)

    @patch("backend.godmode.views.producer")
    def test_api_latency_test(self, producer):
        """Verify that a latency test can be started."""
        ret = self.client.get(GodmodeApi.LATENCY_TEST_URL,
                              {"humes": "some-uuid,anotherUUID"})

        self.assertEqual(ret.status_code, status.HTTP_200_OK)
        producer.latency_test.assert_called()

    def test_api_latency_test_fails_without_params(self):
        """Verify that a latency test can be started."""
        ret = self.client.get(GodmodeApi.LATENCY_TEST_URL)

        self.assertEqual(ret.status_code, status.HTTP_400_BAD_REQUEST)

    def test_api_latency_test_access(self):
        """Verify that only superusers can start a latency test."""
        client = APIClient()
        client.login(username="normie@t.se", password="pw")

        homes = Home.objects.all()
        ret = client.get(GodmodeApi.HUMES_URL.format(homes[0].id))

        self.assertEqual(ret.status_code, status.HTTP_403_FORBIDDEN)
