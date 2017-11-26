"""
User managers
"""
from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    """
    Creates and saves a user
    """
    def _create_user(self, name, email, password, **extra_fields):
        if not name:
            raise ValueError('The given username and email must be set')
        email = self.normalize_email(email)
        name = self.model.normalize_username(name)
        user = self.model(name=name, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, name, email, password=None, is_staff=False,
                    alias=None, avatar=None):
        return self._create_user(name, email, password, is_staff=is_staff,
                                 alias=alias, avatar=avatar)

    def create_superuser(self, name, email, password, alias=None,
                         avatar=None):
        return self._create_user(name, email, password, is_superuser=True,
                                 alias=alias, avatar=avatar)
