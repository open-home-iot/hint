import uuid

from django.test import TestCase

from rest_framework.test import APIClient
from rest_framework import status

# Refer to models under test with an absolute path as the root path of run
# tests are from ../backend.
from backend.user.models import User
from backend.hume.models import Hume


class HumePairApi(TestCase):
    HUME_PAIR_URL = "/api/hume/pair"

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

        Special CSRF handling in this case as the view handles an
        unauthenticated endpoint which should still verify CSRF.
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
