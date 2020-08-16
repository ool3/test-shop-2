from django.db import models
from django.contrib.auth.models import User


class PhoneUser(models.Model):
    username = models.CharField(max_length=122)
    phone = models.CharField(max_length=12)