from django.db import models
from boat.models import BOAT_STATUS

TECH_CHECK_PAYMENT_ACCEPTED = "tech_check_payment_accepted"
TECH_CHECK_PAYMENT_REJECTED = "tech_check_payment_rejected"
REMOVE_REQUEST_ACCEPTED = "remove_request_accepted"

NOTIFICATION_STATUSES = [(TECH_CHECK_PAYMENT_ACCEPTED, "tech check payment accepted"),
                         (TECH_CHECK_PAYMENT_REJECTED, "tech check payment rejected"),
                         (REMOVE_REQUEST_ACCEPTED, "remove request accepted")
                         ] + BOAT_STATUS


class Notification(models.Model):
    owner = models.ForeignKey(to='owner.Owner', on_delete=models.CASCADE)
    boat = models.ForeignKey(to='boat.Boat', null=True, blank=True, on_delete=models.CASCADE)
    status = models.CharField(max_length=250, choices=NOTIFICATION_STATUSES)
    watched = models.BooleanField(default=False)
    extra_data = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.boat.owner.email} - {self.get_status_display()}"