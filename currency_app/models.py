from django.db import models
from django.utils import timezone


class CurrencyRate(models.Model):
    rate = models.DecimalField(max_digits=10, decimal_places=4)
    source = models.CharField(max_length=100)
    currency_pair = models.CharField(max_length=10, default='USD/RUB')
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.currency_pair}: {self.rate} at {self.timestamp}"
