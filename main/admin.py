from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Notification, Fine, RemoveRequest, PaymentRequest, TechCheckRequest


admin.site.register(Notification)
admin.site.register(Fine)
admin.site.register(RemoveRequest)
admin.site.register(PaymentRequest)
admin.site.register(TechCheckRequest)
