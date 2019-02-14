from django.forms import ModelForm

from .models import Owner


class UserForm(ModelForm):
    class Meta:
        model = Owner
        fields = '__all__'