from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser


class Owner(AbstractUser):
    first_name = models.CharField("Имя", max_length=250)
    last_name = models.CharField("Фамилия", max_length=250)
    gender = models.CharField("Пол", max_length=20, choices=[("Мужской", "Мужской"),
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
    is_staff = models.BooleanField(default=False)
    password = models.CharField(max_length=250)

    def __str__(self):
        return self.email


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
    model_type = models.CharField("Тип и модель", max_length=300) # need choices here 
    name = models.CharField("Наименование", max_length=250)
    imo = models.CharField("Идентификационный (IMO)", max_length=250)
    build_place = models.CharField("Место постройки", max_length=300)
    build_year = models.PositiveIntegerField("Год постройки")
    material = models.CharField("Материал корпуса", max_length=200, choices=BOAT_MATERIAL_TYPES)
    length = models.PositiveIntegerField("Длина (м)")
    width = models.PositiveIntegerField("Ширина (м)")
    height_board = models.PositiveIntegerField("Высота борта (м)")
    height_second_board = models.PositiveIntegerField("высота надв. Борта (м)")
    capacity = models.PositiveIntegerField("Вместимость (тонн)")
    capacity_load = models.PositiveIntegerField("Грузоподъемность (кг)")
    passenger_awn = models.PositiveIntegerField("Пассажировместимость (чел.)")
    swimming_place = models.CharField("Район и условия плавания", max_length=300)
    engine_type = models.CharField("Тип главного двигателя", max_length=300) # TODO: add choices
    engine_model = models.CharField("Марка двигателя", max_length=300)
    engine_number = models.CharField("Заводские номера двигателей", max_length=300)
    engine_power = models.PositiveIntegerField("Мощность двигателя/ей (кВт/л.с.)")
    # engine_type = models.CharField("Тип движителя", max_length=300) WTF? Again?
    sails_amount = models.PositiveIntegerField("Количество парусов")
    sail_area = models.PositiveIntegerField("Площадь парусов (м2)")
    prev_numbers_or_name = models.CharField("Прежние регистр. No и название судна", max_length=300)
    prev_registration_place = models.CharField("Место прежней регистрации судна", max_length=300)
    parking_place = models.CharField("Место постоянной стоянки судна", max_length=300)
    passport_image = models.FileField(null=False, blank=False)
    other_files = models.FileField(null=True, blank=False)
    status = models.CharField(max_length=100, choices=BOAT_STATUS)

    def __str__(self):
        return f"{ self.name } - { self.model_type }"


# TODO: think how this model gotta look
class Notification(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    boat = models.ForeignKey(Boat, on_delete=models.CASCADE)

    def __str__(self):
        return self.boat.owner.email


class Fine(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField("Сумма")

    def __str__(self):
        return f"{self.owner.email} - {str(self.amount)}"
