"""
Django models
"""
from __future__ import unicode_literals

from datetime import time

from django.contrib.auth.models import AbstractBaseUser
from django.db import models

from city_issues.user_managers import UserManager

ROLE_ADMIN = 1
ROLE_MODERATOR = 2
ROLE_USER = 3


class Role(models.Model):
    """
    Roles table in the database
    """
    role = models.TextField()

    class Meta:
        """..."""
        managed = False
        db_table = 'roles'


class User(AbstractBaseUser):
    """
    Users table in the database
    """
    name = models.TextField(
        unique=True)
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

    # Connects a custom user manager
    objects = UserManager()

    USERNAME_FIELD = 'name'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name

    @property
    def password(self):
        """..."""
        return self.hashed_password

    @password.setter
    def set_hashed_password(self, raw_password):
        super(User, self).set_password(raw_password)

    @property
    def is_active(self):
        """..."""
        return not self.delete_date

    @is_active.setter
    def set_active(self, value):
        self.delete_date = None if value else time.time.now()

    @property
    def is_staff(self):
        """..."""
        return self.role == ROLE_MODERATOR

    @is_staff.setter
    def set_staff(self, value):
        if value:
            self.role = ROLE_MODERATOR
        else:
            self.role = ROLE_USER

    @property
    def is_superuser(self):
        """..."""
        return self.role == ROLE_ADMIN

    @is_superuser.setter
    def set_superuser(self, value):
        if value:
            self.role = ROLE_ADMIN
        else:
            self.role = ROLE_USER

    @property
    def last_login(self):
        """Added to meet Django AbstractBaseUser interface requirements"""
        return None

    class Meta:
        """..."""
        managed = False
        db_table = 'users'
