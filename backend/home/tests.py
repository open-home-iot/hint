from django.test import TestCase

from rest_framework.test import APIClient
from rest_framework import status

# Refer to models under test with an absolute path as the root path of run
# tests are from ../backend.
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
    HOME_CREATE_URL = "/api/homes/"

    @classmethod
    def setUpClass(cls):
        """
        Sets up global user for authentication.
        """
        super().setUpClass()
        User.objects.create_user(email="suite@t.se", password="pw")

    def setUp(self):
        """
        CALLED PER TEST CASE!

        Create shared test case data, what's created here needs to be torn
        down in tearDown().
        """
        self.client = APIClient()
        # NOTE! Cannot test with CSRF and authentication at the same time for
        # some fucking reason. Post on stackoverflow why, it may help someone.
        # req_client = APIClient()
        # ret = req_client.get("/")
        # self.csrf_value = ret.cookies['csrftoken'].value
        # self.client = APIClient(
        #    enforce_csrf_checks=True,
        #    HTTP_X_CSRFTOKEN=self.csrf_value,
        #    HTTP_COOKIE="csrftoken=" + self.csrf_value
        # )
        self.client.login(username="suite@t.se", password="pw")

    def test_api_create_home(self):
        """
        Verify that a HOME can be created through the API and that the creating
        user is automatically associated with the created HOME instance.
        """
        ret = self.client.post(HomeCreateApi.HOME_CREATE_URL,
                               {'name': 'home1'}, format="json")

        self.assertEqual(ret.status_code, status.HTTP_201_CREATED)

        [home] = Home.objects.all()

        try:
            home.users.get(email='suite@t.se')
        except User.DoesNotExist:
            self.fail("User was not associated with the created HOME.")

        self.assertEqual(ret.data, {'id': 1, 'name': 'home1'})

    def test_api_create_home_fail_no_csrf_token(self):
        """
        Verify that a HOME cannot be created if no CSRF protection is set.
        """
        client_wo_csrf = APIClient(enforce_csrf_checks=True)
        client_wo_csrf.login(username="suite@t.se", password="pw")
        ret = client_wo_csrf.post(HomeCreateApi.HOME_CREATE_URL,
                                  {'name': 'home1'}, format="json")

        self.assertEqual(ret.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            ret.data,
            {'detail': 'CSRF Failed: CSRF cookie not set.'}
        )

    def test_api_create_home_fail_unauthenticated(self):
        """
        Verify that a HOME cannot be created if the user is not authenticated.
        """
        client_wo_authentication = APIClient()

        ret = client_wo_authentication.post(
            HomeCreateApi.HOME_CREATE_URL,
            {'name': 'home1'}
        )

        self.assertEqual(ret.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            ret.data,
            {'detail': 'Authentication credentials were not provided.'}
        )


class HomeGetApi(TestCase):
    HOME_GET_ALL_URL = "/api/homes/"

    @classmethod
    def setUpClass(cls):
        """
        Sets up global user for authentication.
        """
        super().setUpClass()
        User.objects.create_user(email="suite@t.se", password="pw")
        User.objects.create_user(email="some_dude@t.se", password="pw")

    @classmethod
    def tearDownClass(cls):
        """
        Remove global user.
        """
        super().tearDownClass()
        for user in User.objects.all():
            user.delete()

    def setUp(self):
        """
        CALLED PER TEST CASE!

        Create shared test case data, what's created here needs to be torn
        down in tearDown().
        """
        self.client = APIClient()
        self.client.login(username="suite@t.se", password="pw")

    def tearDown(self):
        """
        CALLED PER TEST CASE!

        Clear all created data from setUp() and the run test case.
        """
        for home in Home.objects.all():
            home.delete()

    def test_api_get_all_homes(self):
        """
        Verify an authenticated user can get all home instances belonging to
        the user.
        """
        home = Home.objects.create(name='home1')
        home.users.add(User.objects.get(email='suite@t.se'))
        home.save()
        home = Home.objects.create(name='home2')
        home.users.add(User.objects.get(email='suite@t.se'))
        home.save()

        ret = self.client.get(HomeGetApi.HOME_GET_ALL_URL)

        self.assertEqual(ret.status_code, status.HTTP_200_OK)
        [home1, home2] = ret.data

    def test_api_get_all_homes_only_user_specific_homes(self):
        """
        Verifies only the current user's HOMEs are returned by the GET API.
        """
        home = Home.objects.create(name='home1')
        home.users.add(User.objects.get(email='suite@t.se'))
        home.save()
        home = Home.objects.create(name='home2')
        home.users.add(User.objects.get(email='some_dude@t.se'))
        home.save()

        ret = self.client.get(HomeGetApi.HOME_GET_ALL_URL)

        self.assertEqual(ret.status_code, status.HTTP_200_OK)
        [home] = ret.data
        self.assertEqual(home['name'], 'home1')

    def test_api_get_all_homes_fail_unauthenticated(self):
        """
        Verifies an unauthenticated user cannot access the GET HOME API.
        """
        client_wo_authentication = APIClient()

        ret = client_wo_authentication.get(HomeGetApi.HOME_GET_ALL_URL)

        self.assertEqual(ret.status_code, status.HTTP_403_FORBIDDEN)
