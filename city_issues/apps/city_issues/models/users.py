from __future__ import unicode_literals

from datetime import time

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, name, email, role):
        """
        Creates and saves a User with the given name and email.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            name=self.name,
            email=self.email,
            role=self.role,
        )
        # user.save(using=self._db)
        user.save(using=self.city_issues)
        return user

    def create_superuser(self, name, email, role):
        """
        Creates and saves a superuser with the given name and email.
        """
        user = self.model(
            name=self.name,
            email=self.email,
            role=self.role,
        )
        user.is_admin = True
        # user.save(using=self._db)
        user.save(using=self.city_issues)
        return user


class Role(models.Model):
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
        null=False,
        unique=True)
    hashed_password = models.CharField(
        max_length=30,
        blank=True,
        null=True)
    role = models.ForeignKey(
        'Roles',
        blank=False,
        null=False)
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
    REQUIRED_FIELDS = ['email', 'role']

    @property
    def is_active(self):
        return bool(self.delete_date)

    @is_active.setter
    def set_time(self):
        self.delete_date = time.time.now()

    @property
    def is_staff(self):
        return self.role.id == 2

    @is_staff.setter
    def create_role(self):
        self.role.id = 2

    @property
    def is_superuser(self):
        return self.role.id == 1

    # @is_superuser.setter
    # def create_super_role(self):
    #     self.role.id = 1

    class Meta:
        managed = False
        db_table = 'users'
