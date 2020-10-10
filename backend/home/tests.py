from django.test import TestCase

from rest_framework.test import APIClient
from rest_framework import status

from backend.user.models import User
from backend.home.models import Home


class HomeModel(TestCase):
    def setUp(self):
        """
        CALLED PER TEST CASE!

        Create shared test case data, what's created here needs to be torn
        down in tearDown().
        """
        self.user = User.objects.create_user("t@t.se", password="pw")

    def tearDown(self):
        """
        CALLED PER TEST CASE!

        Clear all created data from setUp() and the run test case.
        """
        for user in User.objects.all():
            user.delete()

        for home in Home.objects.all():
            home.delete()

    def test_create_home(self):
        """
        Verify a HOME model instance can be created.
        """
        home = Home.objects.create(name="home1")
        home.users.add(self.user)
        home.save()


class HomeCreateApi(TestCase):
    HOME_CREATE_URL = "/api/home/"

    @classmethod
    def setUpClass(cls):
        """
        Need class setup to create base user for authentication.
        """
        super().setUpClass()
        user = User.objects.create_user(email="suite@t.se", password="pw")
        print("\nsetUpClass")
        print(f"Created user: {user}")

    @classmethod
    def tearDownClass(cls):
        """
        Clean up user created in setUpClass().
        """
        super().tearDownClass()
        print("\ntearDownClass")
        user = User.objects.get(email="suite@t.se")
        print(f"{user}")

    def setUp(self):
        """
        CALLED PER TEST CASE!

        Create shared test case data, what's created here needs to be torn
        down in tearDown().
        """
        user = User.objects.get(email="suite@t.se")
        print("\nsetUp")
        print(f"User for auth: {user}")
        ret = self.client.get("/")
        self.csrf_value = ret.cookies['csrftoken'].value
        self.client = APIClient(
            enforce_csrf_checks=False,
            HTTP_X_CSRFTOKEN=self.csrf_value,
            HTTP_COOKIE="csrftoken=" + self.csrf_value
        )
        ret = self.client.login(email="suite@t.se", password="pw")

    def tearDown(self):
        """
        CALLED PER TEST CASE!

        Clear all created data from setUp() and the run test case.
        """
        print("\ntearDown")
        print(User.objects.all())

        for home in Home.objects.all():
            home.delete()

    def test_api_create_home(self):
        """
        Verify that a HOME can be created through the API.
        """
        ret = self.client.post(HomeCreateApi.HOME_CREATE_URL,
                               {'name': 'home1'})

        self.assertEqual(ret.status_code, status.HTTP_201_CREATED)

    def test_api_create_home_fail_unauthenticated(self):
        """
        Verify that a HOME cannot be created if the user is not authenticated.
        """
        client_wo_authentication = APIClient(enforce_csrf_checks=True)

        ret = client_wo_authentication.post(
            HomeCreateApi.HOME_CREATE_URL,
            {'name': 'home1'}
        )

        self.assertEqual(ret.status_code, status.HTTP_403_FORBIDDEN)
