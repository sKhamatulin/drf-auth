# from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models


# User = get_user_model()


class CustomUser(AbstractUser):
    contactId = models.CharField(max_length=100,
                                 blank=False,
                                 null=False)