from django.contrib import admin

from .models import Fine, RemoveRequest, PaymentRequest, TechCheckRequest


admin.site.register(Fine)
admin.site.register(RemoveRequest)
admin.site.register(PaymentRequest)
admin.site.register(TechCheckRequest)
