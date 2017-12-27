"""
User managers
"""
from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    """
    Creates and saves a user
    """
    def _create_user(self, name, email, alias, password, **extra_fields):
        if not name:
            raise ValueError('The given email and nickname must be set')
        email = self.normalize_email(email)
        name = self.model.normalize_username(name)
        user = self.model(name=name, email=email, alias=alias, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, name, email, alias, password=None, is_staff=False,
                    avatar=None):
        return self._create_user(name, email, alias, password, is_staff=is_staff,
                                 avatar=avatar)

    def create_superuser(self, name, email, alias, password,
                         avatar=None):
        return self._create_user(name, email, alias, password, is_superuser=True,
                                 avatar=avatar)
