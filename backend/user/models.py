from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, \
                                       BaseUserManager


class CustomUserManager(BaseUserManager):
    """
    Co-locates user creation methods since there are several different types
    of users.
    """

    def create_hume_user(self, hume_uuid, generated_password):
        """Used to create Hume users."""
        user = self.create_user(
            email=f"{str(hume_uuid).replace('-', '')}@fake.com",
            password=generated_password
        )

        user.is_hume = True
        user.save(using=self._db)
        return user

    def create_user(self,
                    email,
                    password='',
                    first_name='',
                    last_name=''):
        """Used to create normal, human, users."""
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,
                         email,
                         password='',
                         first_name='',
                         last_name=''):
        """Used to create superusers."""
        user = self.create_user(
            email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        # A superuser holds ALL roles.
        user.is_superuser = True
        user.is_staff = True
        user.is_hume = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Models a user, which could be either an admin, human, or HUME."""

    email = models.EmailField(unique=True)

    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_hume = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []
