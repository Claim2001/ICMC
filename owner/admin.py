from django.contrib import admin
from .models import Owner
from django.contrib.auth.admin import UserAdmin
from .forms import OwnerChangeForm


class OwnerAdmin(UserAdmin):
    form = OwnerChangeForm

    fieldsets = ()


admin.site.register(Owner, OwnerAdmin)
