"""
User managers
"""
from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    """
    Creates and saves a user
    """
    def _create_user(self, email, alias, name, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        elif not alias:
            raise ValueError('The given alias must be set')
        user = self.model(email=self.normalize_email(email), alias=alias, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, alias, name, password=None, is_staff=False,
                    avatar=None):
        return self._create_user(email=email, password=password, alias=alias, name=name, is_staff=is_staff,
                                 avatar=avatar)

    def create_superuser(self, email, alias, name, password,
                         avatar=None):
        return self._create_user(email=email, password=password, alias=alias, name=name, is_superuser=True,
                                 avatar=avatar)
