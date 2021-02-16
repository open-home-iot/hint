# pylint: disable=missing-class-docstring
import uuid

from django.test import TestCase

from rest_framework.test import APIClient
from rest_framework import status

# Refer to models under test with an absolute path as the root path of run
# tests are from ../backend.
from backend.user.models import User
from backend.home.models import Home
from backend.hume.models import Hume, ValidHume


HUME_BASE_URL = "/api/humes/"


class HumePairApi(TestCase):
    HUME_PAIR_URL = HUME_BASE_URL

    def setUp(self):
        """
        CALLED PER TEST CASE!

        Create shared test case data.
        """
        self.client = APIClient()

    def test_api_pair_hume(self):
        """
        Verify a HUME can be created through the pairing API if no HUME
        matching the provided UUID exists.
        """
        uid = str(uuid.uuid1())
        ValidHume.objects.create(uuid=uid)

        ret = self.client.post(HumePairApi.HUME_PAIR_URL,
                               {"uuid": uid})

        self.assertEqual(ret.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ret.data["uuid"], uid)

    def test_api_pair_hume_again(self):
        """
        Verify a HUME is not re-created when sending another pairing request,
        but that the HUME's pairing state is returned.
        """
        uid = str(uuid.uuid1())
        ValidHume.objects.create(uuid=uid)

        ret = self.client.post(HumePairApi.HUME_PAIR_URL,
                               {"uuid": uid})
        self.assertEqual(ret.status_code, status.HTTP_201_CREATED)

        # And same again...
        ret = self.client.post(HumePairApi.HUME_PAIR_URL,
                               {"uuid": uid})
        self.assertEqual(ret.status_code, status.HTTP_400_BAD_REQUEST)

        [hume] = Hume.objects.all()

    def test_api_pair_hume_fail_invalid_fields(self):
        """
        Verify that HUME pairing fails if any parameter fails validation.
        """
        uid = str(uuid.uuid1())

        ret = self.client.post(HumePairApi.HUME_PAIR_URL,
                               {"uuid": uid + "bad"})

        self.assertEqual(ret.status_code, status.HTTP_400_BAD_REQUEST)
        uuid_error = ["Must be a valid UUID."]
        self.assertEqual(ret.data, {"uuid": uuid_error})

    def test_api_pair_hume_fail_no_matching_valid_hume(self):
        """
        Verify that HUME pairing fails if there is no ValidHume with a matching
        HUME UUID.
        """
        uid = str(uuid.uuid1())

        ret = self.client.post(HumePairApi.HUME_PAIR_URL,
                               {"uuid": uid})

        self.assertEqual(ret.status_code, status.HTTP_403_FORBIDDEN)


class HumeFindApi(TestCase):

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

    def test_api_find_hume(self):
        """
        Verify that a HUME can be found through supplying a correct UUID to the
        find endpoint, given the HUME is unassociated.
        """
        hume = Hume.objects.create(uuid="c4a19f7e0fd911eb97a060f81dbb505c")

        ret = self.client.get(HUME_BASE_URL + hume.uuid)

        self.assertEqual(ret.status_code, status.HTTP_200_OK)

    def test_api_find_hume_fail_hume_already_paired(self):
        """
        Verify that trying to lookup an already paired HUME fails.
        """
        home = Home.objects.create(name="Home1")
        home.users.add(User.objects.get(email="suite@t.se"))
        home.save()
        hume = Hume.objects.create(uuid="c4a19f7e0fd911eb97a060f81dbb505c",
                                   home=home)

        ret = self.client.get(HUME_BASE_URL + hume.uuid)

        self.assertEqual(ret.status_code, status.HTTP_404_NOT_FOUND)

    def test_api_find_hume_fail_faulty_uuid(self):
        """
        Verify that trying to search using a faulty UUID results in a
        validation error.
        """
        Hume.objects.create(uuid="c4a19f7e0fd911eb97a060f81dbb505c")

        ret = self.client.get(HUME_BASE_URL + "not-a-uuid")

        self.assertEqual(ret.status_code, status.HTTP_404_NOT_FOUND)

    def test_api_find_hume_fail_unauthenticated(self):
        """
        Verify that the HUME search API cannot be accessed when
        unauthenticated.
        """
        client_wo_auth = APIClient()
        hume = Hume.objects.create(uuid="c4a19f7e0fd911eb97a060f81dbb505c")

        ret = client_wo_auth.get(HUME_BASE_URL + hume.uuid)

        self.assertEqual(ret.status_code, status.HTTP_403_FORBIDDEN)


class HumeConfirmPairingApi(TestCase):

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

        self.home = Home.objects.create(name="Home1")
        self.home.users.add(User.objects.get(email="suite@t.se"))
        self.home.save()

    def test_api_confirm_pairing(self):
        """
        Verify that a user may confirm pairing of a HUME that belongs to one of
        the user's HOMEs.
        """
        hume = Hume.objects.create(uuid="c4a19f7e0fd911eb97a060f81dbb505c")

        ret = self.client.post(HUME_BASE_URL +
                               hume.uuid +
                               "/confirm-pairing",
                               {"home_id": self.home.id})

        self.assertEqual(ret.status_code, status.HTTP_200_OK)
        hume = Hume.objects.get(uuid=hume.uuid)
        self.assertEqual(hume.home.id, self.home.id)

    def test_api_confirm_pairing_cannot_be_done_twice(self):
        """
        Verify that confirm pairing can only be done once, once a HOME instance
        is linked to the HUME, subsequent requests are blocked. Only HUMEs
        without HOME instances allocated can be paired.
        """
        hume = Hume.objects.create(uuid="c4a19f7e0fd911eb97a060f81dbb505c")

        ret = self.client.post(HUME_BASE_URL +
                               hume.uuid +
                               "/confirm-pairing",
                               {"home_id": self.home.id})

        self.assertEqual(ret.status_code, status.HTTP_200_OK)
        hume = Hume.objects.get(uuid=hume.uuid)
        self.assertEqual(hume.home.id, self.home.id)

        ret = self.client.post(HUME_BASE_URL +
                               str(hume.uuid) +
                               "/confirm-pairing",
                               {"home_id": self.home.id})

        self.assertEqual(ret.status_code, status.HTTP_404_NOT_FOUND)
        hume = Hume.objects.get(uuid=hume.uuid)
        self.assertEqual(hume.home.id, self.home.id)

    def test_api_confirm_pairing_failed_hume_does_not_belong_to_user(self):
        """
        Verify that the confirm pairing action can only be taken for HOMEs
        that belong to the requesting user.
        """
        hume = Hume.objects.create(uuid="c4a19f7e0fd911eb97a060f81dbb505c")
        other_home = Home.objects.create(name="Home2")
        other_home.users.add(User.objects.create_user(email="bogus@bogus.com",
                                                      password="pw"))
        other_home.save()

        ret = self.client.post(HUME_BASE_URL +
                               str(hume.uuid) +
                               "/confirm-pairing",
                               {"home_id": other_home.id})

        self.assertEqual(ret.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(ret.data, None)

    def test_api_confirm_pairing_failed_unauthenticated(self):
        """
        Verify that the confirm pairing action cannot be taken if the request
        is unauthorized.
        """
        hume = Hume.objects.create(uuid="c4a19f7e0fd911eb97a060f81dbb505c")

        unauthenticated_client = APIClient()

        ret = unauthenticated_client.post(HUME_BASE_URL +
                                          str(hume.uuid) +
                                          "/confirm-pairing",
                                          {"home_id": self.home.id})

        self.assertEqual(ret.status_code, status.HTTP_403_FORBIDDEN)

    def test_api_confirm_pairing_failed_no_csrf_token(self):
        """
        Verify that the confirm pairing action cannot be taken if the request
        does not have a CSRF token.
        """
        hume = Hume.objects.create(uuid="c4a19f7e0fd911eb97a060f81dbb505c")

        csrf_less_client = APIClient(enforce_csrf_checks=True)
        csrf_less_client.login(email="suite@t.se", password="pw")

        ret = csrf_less_client.post(HUME_BASE_URL +
                                    str(hume.uuid) +
                                    "/confirm-pairing")

        self.assertEqual(ret.status_code, status.HTTP_403_FORBIDDEN)


class HomeHumesApi(TestCase):
    HOME_BASE_URL = "/api/homes/"

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

        self.hume = Hume.objects.create(
            uuid="c4a19f7e0fd911eb97a060f81dbb505c"
        )

        self.home = Home.objects.create(name="Home1")
        self.home.users.add(User.objects.get(email="suite@t.se"))
        self.home.save()

        self.hume.home = self.home
        self.hume.save()

    def test_api_get_home_humes(self):
        """
        Verify that the HOME HUMEs API endpoint works as intended
        """
        hume2 = Hume.objects.create(uuid="14a19f7e0fd911eb97a060f81dbb505c")
        hume2.home = self.home
        hume2.save()
        Hume.objects.create(uuid="24a19f7e0fd911eb97a060f81dbb505c")

        ret = self.client.get(HomeHumesApi.HOME_BASE_URL +
                              str(self.home.id) + "/humes")

        self.assertEqual(ret.status_code, status.HTTP_200_OK)
        self.assertEqual(len(ret.data), 2)

    def test_api_get_home_humes_fail_unauthenticated(self):
        """
        Verify that no HUMEs can be gotten if the user is not logged in.
        """
        client_wo_auth = APIClient()

        ret = client_wo_auth.get(HomeHumesApi.HOME_BASE_URL +
                                 str(self.home.id) + "/humes")

        self.assertEqual(ret.status_code, status.HTTP_403_FORBIDDEN)

    def test_api_get_home_humes_no_user_leakage(self):
        """
        Verify that other user's homes are not included in the returned query
        set.
        """
        user = User.objects.create_user(email="t@t.se", password="pw")

        hume = Hume.objects.create(uuid="14a19f7e0fd911eb97a060f81dbb505c")

        home = Home.objects.create(name="Home2")
        home.users.add(user)
        home.save()

        hume.home = home
        hume.save()

        client = APIClient()
        client.login(email="t@t.se", password="pw")

        ret = client.get(HomeHumesApi.HOME_BASE_URL +
                         str(home.id) + "/humes")

        self.assertEqual(ret.status_code, status.HTTP_200_OK)
        self.assertEqual(ret.data[0]["uuid"],
                         "14a19f7e-0fd9-11eb-97a0-60f81dbb505c")

    def test_api_get_home_humes_correct_hume_associations(self):
        """
        Verify that if a user has more than one home, that humes belonging to
        a home cannot be gotten by querying another home.
        """
        home_2 = Home.objects.create(name="Home2")
        home_2.users.add(User.objects.get(email="suite@t.se"))
        home_2.save()

        ret = self.client.get(HomeHumesApi.HOME_BASE_URL +
                              str(home_2.id) + "/humes")

        self.assertEqual([], ret.data)
