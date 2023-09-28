from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
import datetime

from .managers import UserAccountManager

# START: User Models and its multi types
# User Models and its multi types


class UserAccount(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=255)
    email = models.EmailField(("email address"), unique=True)

    # START: User types
    is_client = models.BooleanField(default=True)
    is_lawyer = models.BooleanField(default=False)
    is_judge = models.BooleanField(default=False)
    # END: User types

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserAccountManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    def __str__(self):
        return self.email


class Lawyer(models.Model):
    LAWYER_TYPE = [
        ('1', 'Civil'),
        ('2', 'Criminal'),
        ('3', 'Family'),
        ('4', 'Corporate'),
    ]
    user = models.ForeignKey(
        UserAccount,
        on_delete=models.CASCADE,
        related_name="lawyers")
    bar_code = models.CharField(max_length=255)
    chamber_address = models.TextField(null=True, blank=True)
    lawyer_type = models.PositiveSmallIntegerField(
        choices=LAWYER_TYPE, default=1)

    class Meta:
        ordering = ('user__created_at',)

    def __str__(self):
        return f"{self.bar_code}"


class Judge(models.Model):
    user = models.ForeignKey(
        UserAccount,
        on_delete=models.CASCADE,
        related_name="judges")
    bar_code = models.CharField(max_length=255)
    court_address = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ('user__created_at',)

    def __str__(self):
        return f"{self.bar_code}"

# END: User Models and its multi types


# START: User Model Additional Data
# User Model Additional Data

class PreTrial(models.Model):
    user = models.ForeignKey(
        UserAccount,
        on_delete=models.CASCADE,
        related_name="PreTrial")
    case_act = models.TextField()
    details = models.TextField(null=True, blank=True)
    date_registered = models.DateField(default=datetime.date.today)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('date_registered',)

    def __str__(self):
        return f"{self.calories}_{self.created_at}"

# END: User Model Additional Data
