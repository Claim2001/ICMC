from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField, UserChangeForm

from .models import Owner, Boat
from .forms import UserForm

# TODO: can't change password in admin panel

class OwnerChangeForm(UserForm):
    password = ReadOnlyPasswordHashField(label= ("Password"),
        help_text= ("Raw passwords are not stored, so there is no way to see "
                    "this user's password, but you can change the password "
                    "using <a href=\"password/\">this form</a>."))

class OwnerAdmin(admin.ModelAdmin):
    form = UserForm
    change_form = OwnerChangeForm


admin.site.register(Owner, OwnerAdmin)
admin.site.register(Boat)