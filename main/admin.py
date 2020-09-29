from django.contrib import admin

from .models import RemoveRequest, PaymentRequest, TechCheckRequest


admin.site.register(RemoveRequest)
admin.site.register(PaymentRequest)
admin.site.register(TechCheckRequest)
