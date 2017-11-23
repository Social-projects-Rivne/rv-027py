"""
Django models
"""
from __future__ import unicode_literals

import datetime

from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.hashers import make_password
from django.db import models

from city_issues.user_managers import UserManager


class Role(models.Model):
    """
    Roles table in the database
    """
    role = models.TextField()
    app_label = 'city_issues'

    class Meta:
        """..."""
        managed = False
        db_table = 'roles'


ROLE_ADMIN = Role.objects.get(id=1)
ROLE_MODERATOR = Role.objects.get(id=2)
ROLE_USER = Role.objects.get(id=3)


class User(AbstractBaseUser):
    """
    Users table in the database
    """
    name = models.TextField(
        blank=True,
        null=True)
    alias = models.TextField(
        blank=True,
        null=True)
    email = models.EmailField(
        max_length=50,
        unique=True)
    hashed_password = models.TextField(
        max_length=256,
        blank=True,
        null=True)
    role = models.ForeignKey(
        'Role',
        default=ROLE_USER)
    avatar = models.ImageField(
        blank=True,
        null=True)
    delete_date = models.DateTimeField(
        blank=True,
        null=True)
    last_login = models.DateTimeField(
        blank=True,
        null=True)

    # Connects a custom user manager
    objects = UserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    # REQUIRED_FIELDS = ['email']

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name

    @property
    def password(self):
        """..."""
        return self.hashed_password

    @password.setter
    def password(self, raw_password):
        self.set_password(raw_password)

    def set_password(self, raw_password):
        self.hashed_password = make_password(raw_password)
        self._password = raw_password

    @property
    def is_active(self):
        """..."""
        return not self.delete_date

    @is_active.setter
    def is_active(self, value):
        self.delete_date = None if value else datetime.datetime.now()

    @property
    def is_staff(self):
        """..."""
        return self.role == ROLE_MODERATOR

    @is_staff.setter
    def is_staff(self, value):
        if value:
            self.role = ROLE_MODERATOR
        else:
            self.role = ROLE_USER

    @property
    def is_superuser(self):
        """..."""
        return self.role == ROLE_ADMIN

    @is_superuser.setter
    def is_superuser(self, value):
        if value:
            self.role = ROLE_ADMIN
        else:
            self.role = ROLE_USER

    class Meta:
        """..."""
        managed = False
        db_table = 'users'
