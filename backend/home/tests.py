from django.test import TestCase

from backend.user.models import User
from .models import Home


class HomeModel(TestCase):
    def setUp(self):
        """
        CALLED PER TEST CASE!

        Create shared test case data, what's created here needs to be torn
        down in tearDown().
        """
        self.user = User.objects.create_user("t@t.se", password="pw")
        self.user.save()

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
