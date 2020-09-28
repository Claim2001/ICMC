from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models


class Owner(AbstractUser):
    first_name = models.CharField("Имя", max_length=250)
    last_name = models.CharField("Фамилия", max_length=250)
    father_name = models.CharField("Отчество", max_length=250)
    gender = models.CharField("Пол", max_length=20, null=True, blank=True, choices=[("Мужской", "Мужской"),
                                                                                    ("Женский", "Женский")])
    name_of_organization = models.CharField("Название организации", max_length=250, null=True, blank=True)
    address = models.CharField("Адрес", max_length=300, null=True, blank=True)
    mail_index = models.CharField("Почтовый индекс", max_length=100, null=True, blank=True)
    date_of_passport = models.CharField("Дата выдачи и серия паспорта", max_length=200, null=True, blank=True)
    inn = models.CharField("ИНН", max_length=250, null=True, blank=True)
    country = models.CharField("Страна", max_length=250, null=True, blank=True)
    city = models.CharField("Город", max_length=250, null=True, blank=True)
    email = models.EmailField("Email", max_length=300, unique=True, null=False)
    subject = models.CharField("Вид субъекта", max_length=40, null=True, blank=True, choices=[("Физ. лицо", "Физ.лицо"),
                                                                                              ("Юрид. лицо", "Юрид. лицо")])
    is_inspector = models.BooleanField("Является инспектором", default=False)
    phone_number = models.CharField("Номер телефона", max_length=100, default="", null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    activation_code = models.PositiveIntegerField("Код активации", null=True, blank=True)
    activated = models.BooleanField("Активирован", default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.father_name}"