import datetime

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager
from api.managers import UserAccountManager


# START: Managers
class LawyerManager(BaseUserManager):
    """
    Custom manager for the Lawyer model. 
    - Provides a helper method for handling lawyer creation.
    """

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(user__user_type=UserAccount.Roles.LAWYER)


class JudgeManager(BaseUserManager):
    """
    Custom manager for the Judge model. 
    - Provides a helper method for handling judge creation.
    """

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(user__user_type=UserAccount.Roles.JUDGE)
# END: Managers

# START: User Models and its multi types
# User Models and its multi types


class UserAccount(AbstractBaseUser, PermissionsMixin):
    """
    A custom user model with email as the unique identifier and additional fields for user types.

    Fields:
    - name: CharField, max length 255
    - email: EmailField, unique
    - is_client: BooleanField, default True
    - is_lawyer: BooleanField, default False
    - is_judge: BooleanField, default False
    - is_active: BooleanField, default True
    - is_staff: BooleanField, default False
    - is_superuser: BooleanField, default False
    - created_at: DateTimeField, auto_now_add
    - updated_at: DateTimeField, auto_now

    Managers:
    - objects: UserAccountManager

    Required fields:
    - email (USERNAME_FIELD)
    - name (REQUIRED_FIELDS)

    Methods:
    - __str__: returns email
    """
    class Roles(models.TextChoices):
        CLIENT = 'CLIENT', 'Client'
        LAWYER = 'LAWYER', 'Lawyer'
        JUDGE = 'JUDGE', 'Judge'

    name = models.CharField(_("Name of the User"), max_length=255)
    email = models.EmailField(_("Email Address of the User"), unique=True)
    # avatar = models.ImageField(
    #     _("Avatar of the User"), upload_to="avatars/", null=True, blank=True)
    # START: User types
    user_type = models.CharField(
        _("User Type"), max_length=50, choices=Roles.choices, default=Roles.CLIENT)
    # END: User types

    is_active = models.BooleanField(
        _("Boolean definining active status"), default=True)
    is_staff = models.BooleanField(
        _("Boolean definining staff access level"), default=False)
    is_superuser = models.BooleanField(
        _("Boolean definining staff access level"), default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserAccountManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    def __str__(self):
        return self.email


class Lawyer(models.Model):
    """
    A model representing a lawyer.

    Attributes:
    -----------
    user : UserAccount
        The user account associated with the lawyer.
    bar_code : str
        The bar code of the lawyer.
    chamber_address : str
        The address of the lawyer's chamber.
    lawyer_type : int
        The type of lawyer. Can be one of the following:
            1. Civil
            2. Criminal
            3. Family
            4. Corporate
    """
    class Roles(models.TextChoices):
        CIVIL = 'CIVIL', 'Civil'
        CRIMINAL = 'CRIMINAL', 'Criminal'
        FAMILY = 'FAMILY', 'Family'
        CORPORATE = 'CORPORATE', 'Corporate'

    user = models.OneToOneField(
        UserAccount,
        on_delete=models.CASCADE,
        related_name="lawyers")

    enrollment_no = models.CharField(
        _("Bar council Enrollment No for lawyers"), max_length=255)
    registeration_no = models.CharField(
        _("Bar council Registration No for lawyers"), max_length=255, null=True, blank=True)
    chamber_address = models.TextField(
        _("Chamber address for lawyers"), null=True, blank=True)
    lawyer_type = models.CharField(_("Lawyer Types"), max_length=50,
                                   choices=Roles.choices, default=Roles.CIVIL)

    objects = LawyerManager()

    class Meta:
        ordering = ('user__created_at',)

    def __str__(self):
        return f"{self.bar_code}"


class Judge(models.Model):
    """
    A model representing a judge in the legal system.

    Attributes:
        user (UserAccount): The user account associated with the judge.
        bar_code (str): The bar code of the judge.
        court_address (str): The address of the court where the judge presides.

    Meta:
        ordering (tuple): The default ordering for Judge objects, by user creation date.

    Methods:
        __str__(): Returns a string representation of the judge, using their bar code.
    """
    user = models.OneToOneField(
        UserAccount,
        on_delete=models.CASCADE,
        related_name="judges")
    bar_code = models.CharField(
        _("Bar council code for judges"), max_length=255)
    court_address = models.TextField(
        _("Court Address for judges"), null=True, blank=True)

    objects = JudgeManager()

    class Meta:
        ordering = ('user__created_at',)

    def __str__(self):
        return f"{self.bar_code}"

# END: User Models and its multi types


# START: User Model Additional Data
# User Model Additional Data

class PreTrial(models.Model):
    """
    Model representing a pre-trial record for a user.

    Attributes:
        user (ForeignKey): The user account associated with this pre-trial record.
        case_act (TextField): The case act associated with this pre-trial record.
        details (TextField): Additional details about this pre-trial record.
        date_registered (DateField): The date this pre-trial record was registered.
        created_at (DateTimeField): The date and time this pre-trial record was created.
        updated_at (DateTimeField): The date and time this pre-trial record was last updated.
    """
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
