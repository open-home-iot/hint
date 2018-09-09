from django.test import TestCase
from django.db import transaction
from django.db.utils import IntegrityError
from django.contrib.auth import models as auth_models

from psycopg2 import IntegrityError as PIntegrityError

from hume.models import Hume, HumeUser
from device.models import Device


# Create your tests here.
class Create(TestCase):
    def setUp(self):
        """Create shared test case data, what's created here needs to be torn down in tearDown()."""
        hume = Hume.objects.create(pk=1)

        user = auth_models.User.objects.create(username='Mike')
        hume.users.add(user)

        HumeUser.objects.create(related_hume=hume, username='Molly')

    def tearDown(self):
        """Clear all created data from setUp()."""
        for hume in Hume.objects.all():
            hume.delete()

        for hume_user in HumeUser.objects.all():
            hume_user.delete()

        for user in auth_models.User.objects.all():
            user.delete()

    def test_create_additional_hume_user(self):
        """It should not be possible to have two HUME users for the same HUME."""
        hume = Hume.objects.get(pk=1)

        with transaction.atomic():

            try:
                HumeUser.objects.create(related_hume=hume)
                self.fail('Duplicate HUME users were allowed!')

            except IntegrityError or PIntegrityError:
                pass

    def test_create_additional_users(self):
        """It should be possible to have multiple owning users per HUME."""
        hume = Hume.objects.get(pk=1)

        user_two = auth_models.User.objects.create(username='Manny')
        hume.users.add(user_two)

        hume = Hume.objects.get(pk=1)

        self.assertEqual(2, len(hume.users.all()))


class Delete(TestCase):
    def setUp(self):
        """Create shared test case data, what's created here needs to be torn down in tearDown()."""
        hume = Hume.objects.create(pk=1)

        user = auth_models.User.objects.create(username='Mike')
        hume.users.add(user)

        HumeUser.objects.create(related_hume=hume, username='Molly')

    def tearDown(self):
        """Clear all created data from setUp()."""
        for hume in Hume.objects.all():
            hume.delete()

        for hume_user in HumeUser.objects.all():
            hume_user.delete()

        for user in auth_models.User.objects.all():
            user.delete()

    def test_hume_deleted(self):
        """If a HUME is deleted the HUME user related to that HUME should be deleted as well, but no others."""
        hume_two = Hume.objects.create(pk=2)
        HumeUser.objects.create(related_hume=hume_two, username='Milly')

        hume = Hume.objects.get(pk=1)
        hume.delete()

        self.assertEqual(0, len(HumeUser.objects.filter(related_hume=hume)))
        self.assertEqual(1, len(HumeUser.objects.all()))

    def test_user_deleted(self):
        """Deleting one user should not delete the HUME."""
        hume = Hume.objects.get(pk=1)

        user_two = auth_models.User.objects.create(username='Manny')
        hume.users.add(user_two)

        self.assertEqual(2, len(hume.users.all()))

        user_two.delete()

        self.assertEqual(1, len(hume.users.all()))

    def test_all_users_deleted(self):
        """Deleting all associated users should also delete the HUME."""
        hume = Hume.objects.get(pk=1)

        users = hume.users.all()

        for user in users:
            user.delete()

        if Hume.objects.all().exists():
            self.fail('HUME was not deleted when all users were!')
