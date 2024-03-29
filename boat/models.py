from django.db import models
import addrequestions.models
import json
from addrequestions.helpers import send_sms
from notification.models import Notification

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


def get_message_text_by_status(status, boat_name, extra_data=""):
    message_notifications = {
        "look": f"Ваша заявка по судну {boat_name} находится на стадии рассмотрения",
        "rejected": f"Ваша заявка по судну {boat_name} имеет неправильно заполненные поля, исправьте их и попробуйте снова",
        "payment": f"Ваша заявка по судну {boat_name} успешно прошла проверку и ожидает оплаты",
        "payment_rejected": f"Оплата заявки по судну {boat_name} не прошла успешно. Попробуйте еще раз.",
        "inspector_check": f"Оплата заявки по судну {boat_name} прошла успешно. Пожалуйста придите по адресу и дате: {extra_data}"
        f" для проведения осмотра",
    }

    if status in message_notifications:
        return message_notifications[status]

    else:
        return False


class Boat(models.Model):
    owner = models.ForeignKey(to='owner.Owner', on_delete=models.CASCADE)
    model_type = models.CharField("Тип и модель", max_length=300)  # need choices here
    name = models.CharField("Наименование", max_length=250)
    imo = models.CharField("Идентификационный номер (IMO)", max_length=250)
    build_place = models.CharField("Место создания", max_length=300)
    build_year = models.PositiveIntegerField("Год создания")
    material = models.CharField("Материал корпуса", max_length=200)
    length = models.PositiveIntegerField("Длина (м)")
    width = models.PositiveIntegerField("Ширина (м)")
    height_board = models.PositiveIntegerField("Высота борта (м)")
    height_second_board = models.PositiveIntegerField("Высота надводного борта (м)")
    capacity = models.PositiveIntegerField("Вместимость (тонн)")
    capacity_load = models.PositiveIntegerField("Грузоподъемность судна (кг)")
    passenger_awn = models.PositiveIntegerField("Пассажировместимость судна (чел.)")
    swimming_place = models.CharField("Район и условия хождения(плавания)", max_length=300)
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

                sms_message = get_message_text_by_status(status=self.status,
                                                         boat_name=self.name, extra_data=notification.extra_data)

                if sms_message:
                    send_sms(self.owner.phone_number, sms_message)

                if notification.status == "payment_rejected":
                    notification.boat.change_status("payment")

    def get_incorrect_field_labels(self):
        decoded_incorrect_fields = json.loads(self.incorrect_fields)
        return [Boat._meta.get_field(field).verbose_name for field in decoded_incorrect_fields]

    def get_incorrect_field_names(self):
        return json.loads(self.incorrect_fields)

    def __str__(self):
        return f"{self.name} - {self.model_type}"