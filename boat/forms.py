from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.forms import ModelForm
from .models import Boat


class BoatForm(ModelForm):
    class Meta:
        model = Boat
        exclude = (
            "owner",
            "status",
            "incorrect_fields"
        )
        fields = '__all__'