from django.contrib import messages
from django.contrib.auth.decorators import login_required
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
    logger = logging.getLogger(__name__)
    logger.debug(currency)
    if not FavouriteCurrency.objects.filter(user=request.user, currency=currency).exists():
        FavouriteCurrency.objects.create(user=request.user, currency=currency)
    return redirect('currencies:currency_list')


@login_required
def remove_favorite(request, base):
    currency = get_object_or_404(Currency, base=base)
    request.user.favourite_currencies.filter(currency=currency).delete()
    messages.success(request, f"{currency.base} removed from favorites")
    return redirect('currencies:favorites')
