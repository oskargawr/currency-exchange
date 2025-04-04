from currencies.models import Currency, ExchangeRate, FavouriteCurrency
from django.contrib import admin


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('base', 'name', 'symbol')
    search_fields = ('base', 'name')


@admin.register(ExchangeRate)
class ExchangeRateAdmin(admin.ModelAdmin):
    list_display = ('currency', 'date', 'rate')
    list_filter = ('date', 'currency')
    search_fields = ('currency__base', 'currency__name')


@admin.register(FavouriteCurrency)
class FavoriteCurrencyAdmin(admin.ModelAdmin):
    list_display = ('user', 'currency', 'date_added')
    list_filter = ('user', 'currency')
    search_fields = ('user__username', 'currency__base')
