from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# TODO: read whole documentation and build the skeleton for the project
# TODO: build models
# 
# TODO: create normal README so people can see what I am doing

# TODO: make username not unique

class Owner(AbstractUser):
    second_name = models.CharField(max_length=250)
    gender = models.CharField(max_length=20, choices=[("Мужской", "Мужской"),
                                                      ("Женский", "Женский")])
    name_of_organization = models.CharField(max_length=250)
    address = models.CharField(max_length=300)
    mail_index = models.CharField(max_length=100)
    date_of_passport = models.CharField(max_length=200)
    inn = models.CharField(max_length=250)
    country = models.CharField(max_length=250)
    city = models.CharField(max_length=250)
    email = models.EmailField(max_length=300, unique=True, null=False)
    is_inspector = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=100, default="")

    def __str__(self):
        return self.username
