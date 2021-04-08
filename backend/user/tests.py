import unittest

from django.test import TestCase
from django.db import transaction
from django.db.utils import IntegrityError

from rest_framework.test import APIClient
from rest_framework import status

# Refer to models under test with an absolute path as the root path of run
# tests are from ../backend.
from backend.user.models import User


class UserModel(TestCase):
    """Verifies model behavior for the User model"""

    def setUp(self):
        """
        CALLED PER TEST CASE!

        Create shared test case data, what's created here needs to be torn
        down in tearDown().
        """
        user = User.objects.create(email="t@t.se")
        user.set_password("pw")
        user.save()

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


class UserCreateApi(TestCase):
    """Verifies the User creation API"""

    USER_CREATE_URL = "/api/users/signup"

    def setUp(self):
        """
        CALLED PER TEST CASE!

        Create shared test case data, what's created here needs to be torn
        down in tearDown().

        Special CSRF handling in this case as the view handles an
        unauthenticated endpoint which should still verify CSRF.
        """
        self.client = APIClient()

    def test_api_create_user_email_password_only(self):
        """
        Verify a user can be created by supplying only an email address and a
        password.
        """
        ret = self.client.post(UserCreateApi.USER_CREATE_URL,
                               {'email': 't@t.se', 'password': 'pw'})

        self.assertEqual(ret.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ret.data, {'email': 't@t.se',
                                    'first_name': '',
                                    'last_name': ''})
        self.assertEqual(1, len(User.objects.all()))

    def test_api_create_user_with_name(self):
        """
        Verify the user API supports setting a first and last name for a user.
        """
        ret = self.client.post(UserCreateApi.USER_CREATE_URL,
                               {'email': 't@t.se', 'password': 'pw',
                                'first_name': 'test1', 'last_name': 'test2'})
        self.assertEqual(ret.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ret.data, {'email': 't@t.se',
                                    'first_name': 'test1',
                                    'last_name': 'test2'})
        user = User.objects.get(email='t@t.se')
        self.assertEqual(user.first_name, 'test1')
        self.assertEqual(user.last_name, 'test2')

    def test_api_create_user_with_blank_names(self):
        """
        Verify a user cannot be created if first and last name are nulled.
        """
        ret = self.client.post(UserCreateApi.USER_CREATE_URL,
                               {'email': 't@t.se', 'password': 'pw',
                                'first_name': '', 'last_name': ''})
        self.assertEqual(ret.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ret.data,
                         {'email': 't@t.se',
                          'first_name': '',
                          'last_name': ''})
        user = User.objects.get(email='t@t.se')
        self.assertEqual(user.first_name, '')
        self.assertEqual(user.last_name, '')

    def test_api_create_user_fail_email_is_not_an_email(self):
        """
        Verify a user cannot be created if the supplied email is not an email.
        """
        ret = self.client.post(UserCreateApi.USER_CREATE_URL,
                               {'email': 't@t.', 'password': 'pw'})
        self.assertEqual(ret.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(ret.data, {'email': ['Enter a valid email address.']})

    def test_api_create_user_fail_no_email(self):
        """
        Verify a user cannot be created if no email is supplied.
        """
        ret = self.client.post(UserCreateApi.USER_CREATE_URL,
                               {'password': 'pw'})
        self.assertEqual(ret.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(ret.data, {'email': ['This field is required.']})

    def test_api_create_user_fail_no_password(self):
        """
        Verify a user cannot be created if no password is supplied.
        """
        ret = self.client.post(UserCreateApi.USER_CREATE_URL,
                               {'email': 't@t.se'})
        self.assertEqual(ret.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(ret.data, {'password': ['This field is required.']})

    def test_api_create_user_fail_email_already_exists(self):
        """
        Verify a user cannot be created if email already exists.
        """
        User.objects.create(email="t@t.se")

        ret = self.client.post(UserCreateApi.USER_CREATE_URL,
                               {'email': 't@t.se', 'password': 'pw'})
        self.assertEqual(ret.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(ret.data,
                         {'email': ['user with this email already exists.']})

    def test_api_create_user_fail_first_and_last_name_too_long(self):
        """
        Verify a user cannot be created if first and last name exceed character
        limit.
        """
        long_name = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa1"

        ret = self.client.post(UserCreateApi.USER_CREATE_URL,
                               {'email': 't@t.se', 'password': 'pw',
                                'first_name': long_name,
                                'last_name': long_name})
        self.assertEqual(ret.status_code, status.HTTP_400_BAD_REQUEST)
        expected_error_msg = \
            'Ensure this field has no more than 50 characters.'
        self.assertEqual(ret.data,
                         {'first_name': [expected_error_msg],
                          'last_name': [expected_error_msg]})


class UserGetApi(TestCase):
    """Verifies the User fetching API endpoint"""

    USER_GET_SELF_URL = "/api/users/self"

    @classmethod
    def setUpClass(cls):
        """
        Need class setup to create base user for authentication.
        """
        super().setUpClass()
        User.objects.create_user('t@t.se', password='pw')

    def setUp(self):
        """
        CALLED PER TEST CASE!

        Create shared test case data, what's created here needs to be torn
        down in tearDown().

        Login required since GET user is an authenticated view.
        """
        self.client = APIClient()
        self.client.login(email='t@t.se', password='pw')

    def test_api_get_user_self(self):
        """
        Verify user self endpoint returns information about the request's
        authenticated user.
        """
        ret = self.client.get(UserGetApi.USER_GET_SELF_URL)

        self.assertEqual(ret.status_code, status.HTTP_200_OK)
        self.assertEqual(ret.data, {'email': 't@t.se', 'first_name': '',
                                    'last_name': ''})

    def test_api_get_user_self_fail_unauthenticated(self):
        """
        Verify that an unauthenticated request for user self fails.
        """
        client_wo_authentication = APIClient()

        ret = client_wo_authentication.get(UserGetApi.USER_GET_SELF_URL)
        self.assertEqual(ret.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            ret.data,
            {'detail': 'Authentication credentials were not provided.'}
        )


class UserAuthApi(TestCase):
    """Verifies User authentication endpoints"""

    USER_AUTH_LOGIN_URL = "/api/users/login"
    USER_AUTH_LOGOUT_URL = "/api/users/logout"

    @classmethod
    def setUpClass(cls):
        """
        Need class setup to create base user for authentication.
        """
        super().setUpClass()
        User.objects.create_user('t@t.se', password='pw')

    def setUp(self):
        """
        CALLED PER TEST CASE!

        Create shared test case data, what's created here needs to be torn
        down in tearDown().

        Login required since GET user is an authenticated view.
        """
        req_client = APIClient()
        ret = req_client.get("/")
        self.csrf_value = ret.cookies['csrftoken'].value
        self.client = APIClient(
            enforce_csrf_checks=True,
            HTTP_X_CSRFTOKEN=self.csrf_value,
            HTTP_COOKIE="csrftoken=" + self.csrf_value
        )

    def test_api_user_login(self):
        """
        Verify a user with correct credentials can log in.
        """
        ret = self.client.post(UserAuthApi.USER_AUTH_LOGIN_URL,
                               {"username": "t@t.se", "password": "pw"},
                               format="json")

        self.assertEqual(ret.status_code, status.HTTP_200_OK)

    @unittest.skip("CSRF for login disabled")
    def test_api_user_login_fail_no_csrf(self):
        """
        Verify login requests require a CSRF token.
        """
        client = APIClient(enforce_csrf_checks=True)
        ret = client.post(UserAuthApi.USER_AUTH_LOGIN_URL,
                          {"username": "t@t.se", "password": "pw"},
                          format="json")

        self.assertEqual(ret.status_code, status.HTTP_403_FORBIDDEN)

    def test_api_user_login_fail_wrong_method(self):
        """
        Verify a user cannot use any other method than POST to login.
        """
        ret = self.client.get(UserAuthApi.USER_AUTH_LOGIN_URL)

        self.assertEqual(ret.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_api_user_logout(self):
        """
        Verify a user can logout.
        """
        login_successful = self.client.login(username='t@t.se', password='pw')

        self.assertEqual(login_successful, True)

        ret = self.client.post(UserAuthApi.USER_AUTH_LOGOUT_URL)

        self.assertEqual(ret.status_code, status.HTTP_200_OK)

    def test_api_user_logout_fail_wrong_method(self):
        """
        Verify a user cannot use any other method than POST to logout.
        """
        login_successful = self.client.login(username='t@t.se', password='pw')

        self.assertEqual(login_successful, True)

        ret = self.client.get(UserAuthApi.USER_AUTH_LOGOUT_URL)

        self.assertEqual(ret.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
