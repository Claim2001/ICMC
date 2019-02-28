from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.forms import ModelForm

from .models import Owner, Boat


class UserForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Owner
        exclude = (
            "username",
            "superuser_status",
            "user_permissions",
            "last_login",
            "is_staff",
            "is_active",
            "is_superuser",
            "groups",
            "date_joined",
            "is_inspector"
        )
        fields = '__all__'


class OwnerChangeForm(UserForm):
    password = ReadOnlyPasswordHashField(label="Password",
                                         help_text=("Raw passwords are not stored, so there is no way to see "
                                                    "this user's password, but you can change the password "
                                                    "using <a href=\"../password/\">this form</a>."))

    class Meta:
        model = Owner
        fields = '__all__'


class BoatForm(ModelForm):
    class Meta:
        model = Boat
        exclude = (
            "owner",
            "status",
        )
        fields = '__all__'
