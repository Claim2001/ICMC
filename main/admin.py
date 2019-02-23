from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField, UserChangeForm

from .models import Owner, Boat

# TODO: can't change password in admin panel

# class OwnerAdminForm(UserChangeForm):
#     password = ReadOnlyPasswordHashField(label=("Password"),
#         help_text=("Raw passwords are not stored, so there is no way to see "
#                     "this user's password, but you can change the password "
#                     "using <a href=\"../password/\">this form</a>."))

#     class Meta(UserChangeForm.Meta):
#         model = Owner
#         fields = "__all__"


# class OwnerAdmin(admin.ModelAdmin):
#     form = OwnerAdminForm


admin.site.register(Owner)
admin.site.register(Boat)