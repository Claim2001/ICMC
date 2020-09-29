from django.db import models


class Fine(models.Model):
    owner = models.ForeignKey(to='owner.Owner', on_delete=models.CASCADE)
    boat = models.ForeignKey(to='boat.Boat', on_delete=models.CASCADE)
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