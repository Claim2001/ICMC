from django import forms
from django.forms import ModelForm

from .models import Owner


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