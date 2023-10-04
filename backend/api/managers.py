from django.contrib.auth.base_user import BaseUserManager
from django.db.models.query import QuerySet
from django.utils.translation import gettext_lazy as _

# from api.models import UserAccount

class UserAccountManager(BaseUserManager):
    """
    A custom manager for the User model that provides helper methods for creating users and superusers.
    """

    def create_user(self, email, name, password=None):
        """
        Creates and saves a User with the given email, name and password.

        Args:
            email (str): The email address of the user.
            name (str): The name of the user.
            password (str, optional): The password for the user. Defaults to None.

        Raises:
            ValueError: If email or name is not provided.

        Returns:
            User: The created user object.
        """
        if not email:
            raise ValueError("Users must have an email address")
        if not name:
            raise ValueError("Users must have a name")
        user = self.model(
            email=self.normalize_email(email),
            name=name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email: str, name: str, password: str):
        """
        Creates and saves a superuser with the given email, name, and password.

        Args:
            email (str): The email address of the superuser.
            name (str): The name of the superuser.
            password (str): The password for the superuser.

        Returns:
            User: The newly created superuser.
        """

    def create_superuser(self, email, name, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            name=name,
        )
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user