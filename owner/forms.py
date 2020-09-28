from .models import Owner
from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.forms import ModelForm


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


class OwnerChangeForm(UserChangeForm):
    class Meta:
        model = Owner
        fields = '__all__'