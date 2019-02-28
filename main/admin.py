from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from main.forms import OwnerChangeForm
from .models import Owner, Boat, Notification, Fine


class OwnerAdmin(UserAdmin):
    form = OwnerChangeForm
    add_form = OwnerChangeForm

    fieldsets = ()
    add_fieldsets = ()


admin.site.register(Owner, OwnerAdmin)
admin.site.register(Boat)
admin.site.register(Notification)
admin.site.register(Fine)
