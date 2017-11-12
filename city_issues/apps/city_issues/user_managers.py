from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def _create_user(self, name, email, password, **extra_fields):
        """
        Creates and saves a User with the given name, email and password.
        """
        if not name:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        name = self.model.normalize_username(name)
        user = self.model(name=name, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, name, email=None, password=None, is_staff=False, alias=None, avatar=None):
        return self._create_user(name, email, password, is_staff=is_staff, alias=alias, avatar=avatar)

    def create_superuser(self, name, email, password, alias=None, avatar=None):
        return self._create_user(name, email, password, is_superuser=True, alias=alias, avatar=avatar)
