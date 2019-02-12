from django.db import models
from django.contrib.auth.models import AbstractUser

# TODO: read whole documentation and build the skeleton for the project
# TODO: build models
# TODO: custom authentication
# 
# TODO: create normal README so people can see what I am doing

class CustomUser(AbstractUser):
    age = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.username
