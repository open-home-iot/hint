from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, \
                                       BaseUserManager


class CustomUserManager(BaseUserManager):

    def create_user(self,
                    email,
                    password='',
                    first_name='',
                    last_name=''):
        """Used to create normal users."""
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

        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(unique=True)

    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []
