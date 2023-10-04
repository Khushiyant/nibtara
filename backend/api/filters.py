import django_filters

from .models import Judge, Lawyer, PreTrial, UserAccount


class LawyerFilter(django_filters.FilterSet):
    class Meta:
        """
        This class defines the metadata for the UserAccount model's filter fields.
        It specifies the fields to be included in the filter and excludes the password field.
        """
        model = UserAccount
        fields = ['name', 'email', 'user_type']
        exclude = ['password']


class PreTrialFilter(django_filters.FilterSet):
    class Meta:
        """
        This class defines the metadata options for the PreTrial model filter.
        It specifies the model to be used and the fields to be included in the filter.
        """
        model = PreTrial
        fields = "__all__"
