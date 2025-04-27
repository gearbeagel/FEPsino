from django.db import models
from django.conf import settings
import uuid


class Symbol(models.Model):
    name = models.CharField(max_length=50)
    payout_multiplier = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.name


class Spin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='spins')
    bet_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payout = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    result = models.JSONField()
    win_data = models.JSONField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
