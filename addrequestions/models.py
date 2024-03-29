import json
from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from .helpers import send_sms
from owner.models import Owner
from notification.models import Notification, TECH_CHECK_PAYMENT_REJECTED, TECH_CHECK_PAYMENT_ACCEPTED, REMOVE_REQUEST_ACCEPTED


class PaymentRequest(models.Model):
    check_scan = models.FileField(null=False, blank=False)
    boat = models.ForeignKey(to='boat.Boat', on_delete=models.CASCADE)
    owner = models.ForeignKey(to='owner.Owner', on_delete=models.CASCADE)
    payed = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)

    def __str__(self):
        return str(self.boat)


REMOVE_BOAT_REASONS = (
    ("change", "Изменение владельца или места жительства"),
    ("broke", "Износ или поломка судна"),
    ("ticket", "Утеря или порча судового билета"),
)


class RemoveRequest(models.Model):
    owner = models.ForeignKey(to='owner.Owner', on_delete=models.CASCADE)
    boat = models.ForeignKey(to='boat.Boat', on_delete=models.CASCADE)
    reason = models.CharField(max_length=300, choices=REMOVE_BOAT_REASONS)
    ticket = models.FileField(null=True, blank=True)

    def __str__(self):
        return self.boat.name


TECH_CHECK_TYPE = (
    ("first", "первичный"),
    ("year", "ежегодный"),
)


class TechCheckRequest(models.Model):
    owner = models.ForeignKey(to='owner.Owner', on_delete=models.CASCADE)
    boat = models.ForeignKey(to='boat.Boat', on_delete=models.CASCADE)
    check_type = models.CharField(max_length=100, choices=TECH_CHECK_TYPE)
    check_scan = models.FileField(null=False, blank=False)
    payed = models.BooleanField(default=False)
    inspecting = models.BooleanField(default=True)

    def __str__(self):
        return self.boat.name
from django.db import models

# Create your models here.
