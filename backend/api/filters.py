import django_filters
from .models import UserAccount, Entry


class UserFilter(django_filters.FilterSet):
    class Meta:
        model = UserAccount
        fields = "__all__"


class PreTrialFilter(django_filters.FilterSet):
    class Meta:
        model = Entry
        fields = "__all__"
