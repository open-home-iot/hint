from django.test import TestCase
from django.db import transaction
from django.db.utils import IntegrityError

from rest_framework.test import APIClient
from rest_framework import status

from .models import User


class UserModel(TestCase):
    def setUp(self):
        """
        CALLED PER TEST CASE!

        Create shared test case data, what's created here needs to be torn
        down in tearDown().
        """
        user = User.objects.create(email="t@t.se")
        user.set_password("pw")
        user.save()

    def tearDown(self):
        """
        CALLED PER TEST CASE!

        Clear all created data from setUp() and the run test case.
        """
        for user in User.objects.all():
            user.delete()

    def test_create_user_defaults(self):
        """
        Verify a basic create user results in correct default values.
        """
        user = User.objects.create(email='t2@t.se')
        self.assertEqual(user.first_name, '')
        self.assertEqual(user.first_name, '')
        self.assertEqual(user.is_active, True)
        self.assertEqual(user.is_staff, False)
        self.assertEqual(user.is_superuser, False)

    def test_create_user_fail_duplicate_email(self):
        """
        Verify that a user must have a unique email address.
        """
        with transaction.atomic():
            try:
                User.objects.create_user("t@t.se")
                self.fail("Duplicate user email was allowed.")
            except IntegrityError:
                pass


class UserApi(TestCase):
    def setUp(self):
        """
        CALLED PER TEST CASE!

        Create shared test case data, what's created here needs to be torn
        down in tearDown().
        """
        # CSRF checks need to be explicitly enforced on the request factory or
        # it will not be carried out.
        self.client = APIClient(enforce_csrf_checks=True)

    def tearDown(self):
        """
        CALLED PER TEST CASE!

        Clear all created data from setUp() and the run test case.
        """
        for user in User.objects.all():
            user.delete()

    def test_api_create_user_email_password_only(self):
        """
        Verify a user can be created by supplying only an email address and a
        password.
        """
        ret = self.client.post('/api/user/sign-up',
                               {'email': 't@t.se', 'password': 'pw'},
                               format='json')
        self.assertEqual(ret.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ret.data, {'email': 't@t.se',
                                    'first_name': '',
                                    'last_name': ''})
        self.assertEqual(1, len(User.objects.all()))

    def test_api_create_user_with_name(self):
        """
        Verify the user API supports setting a first and last name for a user.
        """
        ret = self.client.post('/api/user/sign-up',
                               {'email': 't@t.se', 'password': 'pw',
                                'first_name': 'test1', 'last_name': 'test2'},
                               format='json')
        self.assertEqual(ret.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ret.data, {'email': 't@t.se',
                                    'first_name': 'test1',
                                    'last_name': 'test2'})
        user = User.objects.get(email='t@t.se')
        self.assertEqual(user.first_name, 'test1')
        self.assertEqual(user.last_name, 'test2')

    def test_api_create_user_fail_email_is_not_an_email(self):
        """
        Verify a user cannot be created if the supplied email is not an email.
        """
        ret = self.client.post('/api/user/sign-up',
                               {'email': 't@t.', 'password': 'pw'})
        self.assertEqual(ret.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(ret.data, {'email': ['Enter a valid email address.']})

    def test_api_create_user_fail_no_email(self):
        """
        Verify a user cannot be created if no email is supplied.
        """
        ret = self.client.post('/api/user/sign-up',
                               {'password': 'pw'})
        self.assertEqual(ret.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(ret.data, {'email': ['This field is required.']})

    def test_api_create_user_fail_no_password(self):
        """
        Verify a user cannot be created if no password is supplied.
        """
        ret = self.client.post('/api/user/sign-up',
                               {'email': 't@t.se'})
        self.assertEqual(ret.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(ret.data, {'password': ['This field is required.']})

    def test_api_create_user_fail_email_already_exists(self):
        """
        Verify a user cannot be created if no password is supplied.
        """
        User.objects.create(email="t@t.se")

        ret = self.client.post('/api/user/sign-up',
                               {'email': 't@t.se', 'password': 'pw'})
        self.assertEqual(ret.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(ret.data,
                         {'email': ['user with this email already exists.']})
