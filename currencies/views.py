from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.management import call_command
from django.db import models
from django.shortcuts import render, get_object_or_404, redirect
from currencies.models import Currency, ExchangeRate, FavouriteCurrency


def currency_list(request):
    currencies = Currency.objects.all()
    return render(request, 'currencies/list.html', {'currencies': currencies})


def currency_detail(request, base):
    currency = get_object_or_404(Currency, base=base)
    rates = ExchangeRate.objects.filter(currency=currency).order_by('-date')[:7]
    return render(request, 'currencies/detail.html', {'currency': currency, 'rates': rates})


@login_required
def favorite_currencies(request):
    favorites = request.user.favourite_currencies.all()
    return render(request, 'currencies/favorites.html', {'favorites': favorites})


@login_required
def add_favorite(request, base):
    currency = get_object_or_404(Currency, base=base)
    if not FavouriteCurrency.objects.filter(user=request.user, currency=currency).exists():
        FavouriteCurrency.objects.create(user=request.user, currency=currency)
    return redirect('currencies:currency_list')


@login_required
def remove_favorite(request, base):
    currency = get_object_or_404(Currency, base=base)
    request.user.favourite_currencies.filter(currency=currency).delete()
    messages.success(request, f"{currency.base} removed from favorites")
    return redirect('currencies:favorites')


@login_required
def fetch_latest_rates(request):
    try:
        call_command('fetch_rates')
        messages.success(request, 'Successfully fetched latest rates')
        return redirect('currencies:currency_list')
    except Exception as e:
        messages.error(request, f'Error fetching rates: {str(e)}')
        return redirect('currencies:currency_list')


def search_currencies(request):
    query = request.GET.get('q', '').strip()

    if query:
        currencies = Currency.objects.filter(
            models.Q(base__icontains=query) | models.Q(name__icontains=query) | models.Q(symbol__icontains=query)
        ).order_by('base')
    else:
        currencies = Currency.objects.all().order_by('base')

    return render(request, 'currencies/currency_rows.html', {'currencies': currencies})
