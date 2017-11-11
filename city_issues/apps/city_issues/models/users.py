from __future__ import unicode_literals

from django.contrib.auth.models import AbstractBaseUser
from django.db import models


class Roles(models.Model):
    role = models.TextField()

    class Meta:
        managed = False
        db_table = 'roles'


class User(AbstractBaseUser):
    """..."""
    name = models.CharField(
        max_length=30,
        blank=True,
        null=True)
    alias = models.CharField(
        max_length=30,
        blank=True,
        null=True)
    email = models.EmailField(
        max_length=30,
        blank=False,
        null=False)
    hashed_password = models.CharField(
        blank=True,
        null=True)
    role = models.ForeignKey(
        'Roles',
        blank=True,
        null=True)
    avatar = models.ImageField(
        blank=True,
        null=True)
    delete_date = models.DateTimeField(
        blank=True,
        null=True)

    USERNAME_FIELD = 'name'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    class Meta:
        managed = False
        db_table = 'users'
