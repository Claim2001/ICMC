import json

from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser


class Owner(AbstractUser):
    first_name = models.CharField("Имя", max_length=250)
    last_name = models.CharField("Фамилия", max_length=250)
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
    is_inspector = models.BooleanField("Является инспектором", default=False)
    phone_number = models.CharField("Номер телефона", max_length=100, default="", null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    activation_code = models.PositiveIntegerField("Код активации", null=True, blank=True)
    activated = models.BooleanField("Активирован", default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


BOAT_MATERIAL_TYPES = [
    ("wood", "wood"),
    ("other", "other"),
]

BOAT_STATUS = [
    ("wait", "wait"),
    ("look", "look"),
    ("rejected", "rejected"),
    ("payment", "waiting for payment"),
    ("payment_check", "waiting for payment check"),
    ("payment_rejected", "payment rejected"),
    ("inspector_check", "waiting for data check"),
    ("accepted", "accepted"),
]


class Boat(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    model_type = models.CharField("Тип и модель", max_length=300)  # need choices here
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
    engine_type = models.CharField("Тип главного двигателя", max_length=300)  # TODO: add choices
    engine_model = models.CharField("Марка двигателя", max_length=300)
    engine_number = models.CharField("Заводские номера двигателей", max_length=300)
    engine_power = models.PositiveIntegerField("Мощность двигателя/ей (кВт/л.с.)")
    # engine_type = models.CharField("Тип движителя", max_length=300) WTF? Again?
    sails_amount = models.PositiveIntegerField("Количество парусов")
    sail_area = models.PositiveIntegerField("Площадь парусов (м2)")
    prev_numbers_or_name = models.CharField("Прежние регистр. No и название судна", default="", null=True, blank=True,
                                            max_length=300)
    prev_registration_place = models.CharField("Место прежней регистрации судна", default="", null=True, blank=True,
                                               max_length=300)
    parking_place = models.CharField("Место постоянной стоянки судна", max_length=300)
    passport_image = models.FileField("Скан паспорта", null=True, blank=True)
    other_files = models.FileField("Другие файлы", null=True, blank=True)
    status = models.CharField(max_length=100, choices=BOAT_STATUS, default="wait")
    incorrect_fields = models.TextField(default="[]")

    def change_status(self, value):
        not_send_notification_statuses = (
            "wait",
            "payment_check",
            "inspector_check",
        )

        if self.status is not value:
            self.status = value
            self.save()

            if self.status not in not_send_notification_statuses:
                notification = Notification(owner=self.owner, boat=self, status=self.status)
                notification.save()

                if notification.status == "payment_rejected":
                    notification.boat.change_status("payment")

    def get_incorrect_field_labels(self):
        decoded_incorrect_fields = json.loads(self.incorrect_fields)
        return [Boat._meta.get_field(field).verbose_name for field in decoded_incorrect_fields]

    def get_incorrect_field_names(self):
        return json.loads(self.incorrect_fields)

    def __str__(self):
        return f"{self.name} - {self.model_type}"


class Fine(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    boat = models.ForeignKey(Boat, on_delete=models.CASCADE)
    reason = models.CharField(max_length=500)
    amount = models.PositiveIntegerField("Сумма")
    payed = models.BooleanField(default=False)
    inspecting = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.owner.email} - {str(self.amount)}"


class FinePaymentRequest(models.Model):
    fine = models.ForeignKey(Fine, on_delete=models.CASCADE)
    check_scan = models.FileField(null=False, blank=False)
    payed = models.BooleanField(default=False)
    inspecting = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.fine.owner} {self.fine.amount} сум"


class PaymentRequest(models.Model):
    check_scan = models.FileField(null=False, blank=False)
    boat = models.ForeignKey(Boat, on_delete=models.CASCADE)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
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
    boat = models.ForeignKey(Boat, on_delete=models.CASCADE)
    reason = models.CharField(max_length=300, choices=REMOVE_BOAT_REASONS)
    ticket = models.FileField(null=True, blank=True)

    def __str__(self):
        return self.boat.name


TECH_CHECK_TYPE = (
    ("first", "первичный"),
    ("year", "ежегодный"),
)


class TechCheckRequest(models.Model):
    boat = models.ForeignKey(Boat, on_delete=models.CASCADE)
    check_type = models.CharField(max_length=100, choices=TECH_CHECK_TYPE)

    def __str__(self):
        return self.boat.name


class Notification(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    boat = models.ForeignKey(Boat, on_delete=models.CASCADE)
    status = models.CharField(max_length=250, choices=BOAT_STATUS)
    watched = models.BooleanField(default=False)
    extra_data = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.boat.owner.email} - {self.get_status_display()}"



