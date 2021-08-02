"""
Sample user/profile models for testing.  These aren't enabled by default in the
sandbox
"""

from django.contrib.auth.models import (
    AbstractUser, BaseUserManager, AbstractBaseUser)
from django.db import models
from django.utils import timezone

from oscar.core import compat
from oscar.apps.customer import abstract_models


class Profile(models.Model):
    """
    Dummy profile model used for testing
    """
    user = models.OneToOneField(compat.AUTH_USER_MODEL, related_name="profile",
                                on_delete=models.CASCADE)
    MALE, FEMALE = 'M', 'F'
    choices = (
        (MALE, 'Male'),
        (FEMALE, 'Female'))
    gender = models.CharField(max_length=1, choices=choices,
                              verbose_name='Gender')
    age = models.PositiveIntegerField(verbose_name='Age')


# A simple extension of the core User model for Django 1.5+
class ExtendedUserModel(AbstractUser):
    twitter_username = models.CharField(max_length=255, unique=True)


class CustomUserManager(BaseUserManager):

    def create_user(self, mobile_number, password=None):
        now = timezone.now()
        # email = BaseUserManager.normalize_email(email)
        user = self.model(mobile_number=mobile_number, last_login=now)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, mobile_number, password):
        return self.create_user(mobile_number, password)

# A user model which doesn't extend AbstractUser
class CustomUserModel(AbstractBaseUser):
    name = models.CharField(max_length=255, blank=True)
    # email = models.EmailField(unique=True)
    mobile_number = models.PositiveBigIntegerField(unique=True)
    twitter_username = models.CharField(max_length=255, unique=True)

    # USERNAME_FIELD = 'email'
    USERNAME_FIELD = 'mobile_number'

    objects = CustomUserManager()

    def __str__(self):
        return self.mobile_number

    def get_full_name(self):
        return self.name

    get_short_name = get_full_name

# A simple extension of the core Oscar User model
class ExtendedOscarUserModel(abstract_models.AbstractUser):
    twitter_username = models.CharField(max_length=255, unique=True)
