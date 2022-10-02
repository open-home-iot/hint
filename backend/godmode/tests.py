from unittest import TestCase

from rest_framework.test import APIClient
from rest_framework import status

from backend.user.models import User
from backend.home.models import Home

from backend.godmode.views import Homes as GodmodeHomes


class GodmodeApi(TestCase):

    URL = "/api/godmode/{}"

    @classmethod
    def setUpClass(cls):
        """
        Sets up global user for authentication.
        """
        super().setUpClass()
        print("set up class")
        User.objects.create_superuser(email="super@t.se", password="pw")
        User.objects.create_user(email="normie@t.se", password="pw")

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        print("tear down class")
        User.objects.get(email="super@t.se").delete()
        User.objects.get(email="normie@t.se").delete()
        Home.objects.all().delete()

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
        ret = self.client.get(GodmodeApi.URL.format("homes"))

        self.assertEqual(ret.status_code, status.HTTP_200_OK)

    def test_api_get_homes_pagination(self):
        """
        Verify that a superuser can get HOMEs through the godmode endpoint for
        homes.
        """
        for i in range(8):
            Home.objects.create(name="home" + str(i))

        ret = self.client.get(GodmodeApi.URL.format("homes"))

        self.assertEqual(ret.status_code, status.HTTP_200_OK)
        print(ret.data)
        self.assertEqual(len(ret.data["results"]), GodmodeHomes.default_limit)
