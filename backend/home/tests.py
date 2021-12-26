import uuid

from unittest.mock import patch, ANY

from django.test import TestCase

from rest_framework.test import APIClient
from rest_framework import status

# Refer to models under test with an absolute path as the root path of run
# tests are from ../backend.
from backend.user.models import User
from backend.home.models import Home, Room
from backend.hume.models import Hume


class HomeModel(TestCase):

    def setUp(self):
        """
        CALLED PER TEST CASE!

        Create shared test case data. DB instances are automatically deleted
        when each test case ends and do not need to be removed.
        """
        self.user = User.objects.create_user("t@t.se", password="pw")
        self.home = Home.objects.create(name="home1")
        self.home.users.add(self.user)
        self.home.save()

    def test_delete_home_cascade_works(self):
        """
        Verify deleting a home also deletes all its humes.
        """
        hume_user_1 = User.objects.create_hume_user(str(uuid.uuid4()), "pw")
        hume_1 = Hume.objects.create(
            uuid=str(uuid.uuid4()), hume_user=hume_user_1
        )
        hume_1.home = self.home
        hume_1.save()
        hume_user_2 = User.objects.create_hume_user(str(uuid.uuid4()), "pw")
        hume_2 = Hume.objects.create(
            uuid=str(uuid.uuid4()), hume_user=hume_user_2
        )
        hume_2.home = self.home
        hume_2.save()

        self.assertEqual(len(Hume.objects.all()), 2)
        self.home.delete()
        self.assertEqual(len(Hume.objects.all()), 0)


class HomesApi(TestCase):

    URL = "/api/homes"

    @classmethod
    def setUpClass(cls):
        """
        Sets up global user for authentication.
        """
        super().setUpClass()
        User.objects.create_user(email="suite@t.se", password="pw")
        User.objects.create_user(email="some_dude@t.se", password="pw")

    def setUp(self):
        """
        CALLED PER TEST CASE!

        Create shared test case data.
        """
        self.client = APIClient()
        self.client.login(username="suite@t.se", password="pw")

    def test_api_create_home(self):
        """
        Verify that a HOME can be created through the API and that the creating
        user is automatically associated with the created HOME instance.
        """
        ret = self.client.post(HomesApi.URL,
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
        ret = client_wo_csrf.post(HomesApi.URL,
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
            HomesApi.URL,
            {'name': 'home1'}
        )

        self.assertEqual(ret.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            ret.data,
            {'detail': 'Authentication credentials were not provided.'}
        )

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

        ret = self.client.get(HomesApi.URL)

        self.assertEqual(ret.status_code, status.HTTP_200_OK)
        [_home, _home2] = ret.data

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

        ret = self.client.get(HomesApi.URL)

        self.assertEqual(ret.status_code, status.HTTP_200_OK)
        [home] = ret.data
        self.assertEqual(home['name'], 'home1')

    def test_api_get_all_homes_fail_unauthenticated(self):
        """
        Verifies an unauthenticated user cannot access the GET HOME API.
        """
        client_wo_authentication = APIClient()

        ret = client_wo_authentication.get(HomesApi.URL)

        self.assertEqual(ret.status_code, status.HTTP_403_FORBIDDEN)


class HomeSingleApi(TestCase):

    URL = "/api/homes/{}"

    @classmethod
    def setUpClass(cls):
        """
        Sets up global user for authentication.
        """
        super().setUpClass()
        User.objects.create_user(email="suite@t.se", password="pw")

    def setUp(self):
        self.client = APIClient()
        self.client.login(username="suite@t.se", password="pw")

        self.home = Home.objects.create(name="home")
        self.home.users.add(User.objects.get(email="suite@t.se"))

    def test_api_get_home(self):
        """
        Get a single home.
        """
        res = self.client.get(HomeSingleApi.URL.format(self.home.id))

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["id"], 1)

    def test_api_get_home_authauthorized(self):
        """
        Tests the endpoint authentication, same for all methods so no need to
        re-test for others.
        """
        User.objects.create_user(email="t@t.se", password="pw")
        api_client = APIClient()
        api_client.login(username="t@t.se", password="pw")

        res = api_client.get(HomeSingleApi.URL.format(self.home.id))

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(res.data, None)

    def test_api_change_home_name(self):
        """
        Change a home's name.
        """
        new_name = "new_name"
        res = self.client.patch(HomeSingleApi.URL.format(self.home.id),
                                {"name": new_name})

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["name"], new_name)
        # Confirm change in DB as well
        self.assertEqual(Home.objects.get(id=self.home.id).name, new_name)

    def test_api_change_home_name_failed_too_long(self):
        """
        Verify changing a home name fails if the name exceeds the column size.
        """
        too_long_name = "abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
        res = self.client.patch(HomeSingleApi.URL.format(self.home.id),
                                {"name": too_long_name})

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_api_delete_home(self):
        """
        Delete a home.
        """
        res = self.client.delete(HomeSingleApi.URL.format(self.home.id))

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, None)
        with self.assertRaises(Home.DoesNotExist):
            Home.objects.get(id=self.home.id)


class HomeRoomsApi(TestCase):

    URL = "/api/homes/{}/rooms"

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

        Create shared test case data.
        """
        self.client = APIClient()
        self.client.login(username="suite@t.se", password="pw")

        self.home = Home.objects.create(name="home")
        self.home.users.add(User.objects.get(email="suite@t.se"))

    def test_create_room(self):
        """Test creating a Room instance through the API."""
        res = self.client.post(HomeRoomsApi.URL.format(self.home.id),
                               {"name": "test"})

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data["name"], "test")
        self.assertEqual(res.data["id"], 1)

    def test_verify_other_users_cannot_create_room(self):
        """
        Verify that a user cannot create a room for a home that user does not
        own.
        """
        user = User.objects.create_user(email="o@o.se", password="pw")
        home2 = Home.objects.create(name="home2")
        home2.users.add(user)

        res = self.client.post(HomeRoomsApi.URL.format(home2.id),
                               {"name": "test"})

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_all_rooms_of_home(self):
        """Verify that rooms associated to a home can be gotten."""
        Room.objects.create(home=self.home, name="room1")

        res = self.client.get(HomeRoomsApi.URL.format(self.home.id))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        [_room] = res.data

    def test_verify_no_rooms_leak_between_homes(self):
        """
        Verify that if multiple homes exist, each with individual rooms, no
        rooms leak when rooms of one home is queried for.
        """
        Room.objects.create(home=self.home, name="room")

        home2 = Home.objects.create(name="home2")
        home2.users.add(User.objects.get(email="suite@t.se"))
        home2.save()
        Room.objects.create(name="living", home=home2)
        Room.objects.create(name="toilet", home=home2)

        res = self.client.get(HomeRoomsApi.URL.format(self.home.id))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        [room] = res.data
        self.assertEqual(room["name"], "room")

        # Fetch rooms associated to the other home, should be 2 of them.
        res = self.client.get(HomeRoomsApi.URL.format(home2.id))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        [room1, room2] = res.data
        if room1["name"] != "living" and room1["name"] != "toilet":
            self.fail("room1 does not match either of the created rooms")

        if room2["name"] != "living" and room2["name"] != "toilet":
            self.fail("room2 does not match either of the created rooms")

    def test_no_rooms_leak_between_users(self):
        """Verify rooms cannot be gotten by users not owning the home."""
        User.objects.create_user(email="t@t.se", password="password")

        client = APIClient()
        client.login(username="t@t.se", password="password")

        # Not this user's home instance.
        res = client.get(HomeRoomsApi.URL.format(self.home.id))

        self.assertEqual(len(res.data), 0)


class HomeDiscoverDevicesApi(TestCase):

    URL = "/api/homes/{}/devices/discover"

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
        self.client.login(email="suite@t.se", password="pw")

        hume_user = User.objects.create_hume_user(str(uuid.uuid4()), "pw")

        self.hume = Hume.objects.create(
            uuid="c4a19f7e-0fd9-11eb-97a0-60f81dbb505c",
            hume_user=hume_user
        )

        self.home = Home.objects.create(name="Home1")
        self.home.users.add(User.objects.get(email="suite@t.se"))
        self.home.save()

        self.hume.home = self.home
        self.hume.save()

    @patch("backend.home.views.producer")
    def test_discover_devices(self, producer):
        """Verify the discover devices action."""
        res = self.client.get(
            HomeDiscoverDevicesApi.URL.format(self.home.id)
        )

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        producer.discover_devices.assert_called_with(self.hume.uuid, ANY)

    @patch("backend.home.views.producer")
    def test_discover_devices_fail_no_such_hume(self, producer):
        """
        Verify that URL pieces must point to a hume the user owns.
        """
        # Home ID is wrong
        res = self.client.get(
            HomeDiscoverDevicesApi.URL.format(1337)
        )

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

        # Wrong user, access denied
        user = User.objects.create_user(email="t@t.se", password="pw")
        client = APIClient()
        client.login(username=user.email, password="pw")

        # Hume does not belong to the current user
        res = client.get(
            HomeDiscoverDevicesApi.URL.format(self.home.id, self.hume.uuid)
        )

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

        # Home has no humes
        self.hume.delete()

        res = self.client.get(
            HomeDiscoverDevicesApi.URL.format(self.home.id)
        )

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

        # Generally...
        producer.discover_devices.assert_not_called()

    @patch("backend.home.views.producer")
    def test_discover_devices_for_home_with_more_than_one_hume(self, producer):
        """Verify the discover devices action."""
        Hume.objects.create(
            uuid="ef59d369-40dd-4af9-853e-63707e72c61e",
            home=self.home
        )

        res = self.client.get(
            HomeDiscoverDevicesApi.URL.format(self.home.id)
        )

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(producer.discover_devices.call_count, 2)
