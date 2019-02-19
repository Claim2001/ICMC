from django.db import models
from django.contrib.auth.models import AbstractUser

# TODO: read whole documentation and build the skeleton for the project
# TODO: build models
# 
# TODO: create normal README so people can see what I am doing


class Owner(AbstractUser):
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
    password = models.CharField(max_length=300)

    def __str__(self):
        return self.username


BOAT_MATERIAL_TYPES = [
    ("wood", "wood"),
    ("other", "other"),
]

BOAT_STATUS = [
    ("wait", "wait"),
    ("look", "look"),
    ("rejected", "rejected"),
    ("payment", "waiting for payment"),
    ("accepted", "accepted"),
]


# TODO: add date
class Boat(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    model_type = models.CharField(max_length=300)
    name = models.CharField(max_length=250)
    imo = models.CharField(max_length=250)
    build_place = models.CharField(max_length=300)
    build_year = models.PositiveIntegerField()
    material = models.CharField(max_length=200, choices=BOAT_MATERIAL_TYPES)
    length = models.PositiveIntegerField()
    width = models.PositiveIntegerField()
    height_board = models.PositiveIntegerField()
    height_second_board = models.PositiveIntegerField()
    capacity = models.PositiveIntegerField()
    capacity_load = models.PositiveIntegerField()
    passenger_awn = models.PositiveIntegerField()
    swimming_place = models.CharField(max_length=300)
    engine_type = models.CharField(max_length=300) # TODO: add choices
    engine_model = models.CharField(max_length=300)
    engine_power = models.PositiveIntegerField()
    # engine_type = models.CharField(max_length=300) WTF? Again?
    sails_amount = models.PositiveIntegerField()
    sail_area = models.PositiveIntegerField()
    prev_numbers_or_name = models.CharField(max_length=300)
    prev_registration_place = models.CharField(max_length=300)
    parking_place = models.CharField(max_length=300)
    status = models.CharField(max_length=100, choices=BOAT_STATUS)

    def __str__(self):
        return f"{ self.name } - { self.model_type }"
    