import uuid

from django.test import TestCase

from rest_framework.test import APIClient
from rest_framework import status

# Refer to models under test with an absolute path as the root path of run
# tests are from ../backend.
from backend.user.models import User
from backend.home.models import Home
from backend.hume.models import Hume


class HumePairApi(TestCase):
    HUME_PAIR_URL = "/api/hume/pair"

    def setUp(self):
        """
        CALLED PER TEST CASE!

        Create shared test case data, what's created here needs to be torn
        down in tearDown().
        """
        self.client = APIClient()

    def test_api_pair_hume(self):
        """
        Verify a HUME can be created through the pairing API if no HUME
        matching the provided UUID exists.
        """
        uid = str(uuid.uuid1())
        ret = self.client.post(HumePairApi.HUME_PAIR_URL,
                               {"uuid": uid, "ip_address": "127.0.0.1"})

        self.assertEqual(ret.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ret.data["uuid"], uid)
        self.assertEqual(ret.data["ip_address"], "127.0.0.1")
        self.assertEqual(ret.data["is_paired"], False)
        self.assertEqual(ret.data["name"], "")
        self.assertEqual(ret.data["home"], None)

    def test_api_pair_hume_again(self):
        """
        Verify a HUME is not re-created when sending another pairing request,
        but that the HUME's pairing state is returned.
        """
        uid = str(uuid.uuid1())
        ret = self.client.post(HumePairApi.HUME_PAIR_URL,
                               {"uuid": uid, "ip_address": "127.0.0.1"})

        self.assertEqual(ret.status_code, status.HTTP_201_CREATED)

        ret = self.client.post(HumePairApi.HUME_PAIR_URL,
                               {"uuid": uid, "ip_address": "127.0.0.1"})

        self.assertEqual(ret.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(ret.data, {"is_paired": False})

        [hume] = Hume.objects.all()

    def test_api_pair_hume_fail_invalid_fields(self):
        """
        Verify that HUME pairing fails if any parameter fails validation.
        """
        uid = str(uuid.uuid1())
        ret = self.client.post(HumePairApi.HUME_PAIR_URL,
                               {"uuid": uid + "bad", "ip_address": "127.0.0"})

        self.assertEqual(ret.status_code, status.HTTP_400_BAD_REQUEST)
        uuid_error = ["Must be a valid UUID."]
        ip_error = ["Enter a valid IPv4 or IPv6 address."]
        self.assertEqual(ret.data, {"uuid": uuid_error,
                                    "ip_address": ip_error})


class HumeFindApi(TestCase):
    HUME_FIND_URL = "/api/hume/find"

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
        Hume.objects.create(ip_address="127.0.0.1",
                            uuid="c4a19f7e0fd911eb97a060f81dbb505c")

        ret = self.client.get(HumeFindApi.HUME_FIND_URL +
                              "?hume_uuid=c4a19f7e0fd911eb97a060f81dbb505c")

        self.assertEqual(ret.status_code, status.HTTP_200_OK)
        self.assertEqual(ret.data["uuid"],
                         "c4a19f7e-0fd9-11eb-97a0-60f81dbb505c")

    def test_api_find_hume_fail_hume_already_associated(self):
        """
        Verify that trying to lookup an already associated HUME fails.
        """
        home = Home.objects.create(name="Home1")
        home.users.add(User.objects.get(email="suite@t.se"))
        home.save()
        Hume.objects.create(ip_address="127.0.0.1",
                            uuid="c4a19f7e0fd911eb97a060f81dbb505c",
                            home=home)

        ret = self.client.get(HumeFindApi.HUME_FIND_URL +
                              "?hume_uuid=c4a19f7e0fd911eb97a060f81dbb505c")

        self.assertEqual(ret.status_code, status.HTTP_404_NOT_FOUND)

    def test_api_find_hume_fail_faulty_uuid(self):
        """
        Verify that trying to search using a faulty UUID results in a
        validation error.
        """
        Hume.objects.create(ip_address="127.0.0.1",
                            uuid="c4a19f7e0fd911eb97a060f81dbb505c")

        ret = self.client.get(HumeFindApi.HUME_FIND_URL +
                              "?hume_uuid=1234-bbb")

        self.assertEqual(ret.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(ret.data, {"hume_uuid": ["Invalid UUID."]})

    def test_api_find_hume_fail_unauthenticated(self):
        """
        Verify that the HUME search API cannot be accessed when
        unauthenticated.
        """
        client_wo_auth = APIClient()

        ret = client_wo_auth.get(HumeFindApi.HUME_FIND_URL)

        self.assertEqual(ret.status_code, status.HTTP_403_FORBIDDEN)
