from django.contrib.auth.models import AbstractUser
from django.db import models

from user.manager import UserManager


class User(AbstractUser):
    is_field_owner = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=20, unique=True)
    email = models.EmailField(null=True, blank=True)
    username = models.CharField(max_length=150, blank=True, null=True)

    USERNAME_FIELD = 'phone_number'

    objects = UserManager()

    def __str__(self):
        return self.phone_number
