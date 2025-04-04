from django.contrib.auth.models import User
from django.db import models


class Currency(models.Model):
    base = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'currencies'
        ordering = ['base']

    def __str__(self):
        return f"{self.base} - {self.name}"


class ExchangeRate(models.Model):
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='exchange_rates')
    date = models.DateField()
    rate = models.DecimalField(max_digits=20, decimal_places=6)

    class Meta:
        unique_together = ('currency', 'date')
        ordering = ['-date', 'currency']

    def __str__(self):
        return f"{self.currency.base} - {self.rate} on {self.date}"


class FavouriteCurrency(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favourite_currencies')
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='favourited_by')
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'currency')
        verbose_name_plural = 'favourite currencies'

    def __str__(self):
        return f"{self.user.username}'s favourite - {self.currency.base} added on {self.date_added}"
