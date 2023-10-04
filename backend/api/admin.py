from django.contrib import admin
from .models import PreTrial, UserAccount, Lawyer, Judge


admin.site.register(PreTrial)
admin.site.register(UserAccount)
admin.site.register(Lawyer)
admin.site.register(Judge)
