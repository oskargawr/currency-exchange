from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.test import TestCase, RequestFactory
from django.urls import reverse

from currencies.models import Currency, FavouriteCurrency, ExchangeRate
from currencies.views import (
    currency_list,
    currency_detail,
    remove_favorite,
    add_favorite,
    favorite_currencies,
)


class CurrencyListTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="testuser", password="passsword")
        cls.admin = User.objects.create_superuser(username="admin", password="password")

        cls.usd = Currency.objects.create(base="USD", name="US Dollar", symbol="$")
        cls.eur = Currency.objects.create(base="EUR", name="Euro", symbol="€")

        ExchangeRate.objects.create(currency=cls.usd, date="2023-01-01", rate=1.0)
        ExchangeRate.objects.create(currency=cls.eur, date="2023-01-01", rate=0.92)

        FavouriteCurrency.objects.create(user=cls.user, currency=cls.usd)


def test_currency_list_view(self):
    request = RequestFactory().get(reverse("currencies:currency_list"))

    response = currency_list(request)

    self.assertEqual(response.status_code, 200)
    self.assertIn("page_obj", response.context_data)

    paginator = Paginator(Currency.objects.all(), 10)
    self.assertEqual(
        response.context_data["page_obj"].object_list.count(), paginator.count
    )


def test_currency_detail_view(self):
    request = RequestFactory().get(reverse("currencies:currency_detail", args=["USD"]))

    response = currency_detail(request, "USD")

    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.context_data["currency"].base, "USD")
    self.assertEqual(len(response.context_data["rates"]), 1)


def test_favorite_currencies_view(self):
    request = RequestFactory().get(reverse("currencies:favorites"))
    request.user = self.user

    response = favorite_currencies(request)

    self.assertEqual(response.status_code, 200)
    self.assertEqual(len(response.context_data["favorites"]), 1)


def test_add_favorite_view(self):
    request = RequestFactory().get(reverse("currencies:add_favorite", args=["EUR"]))
    request.user = self.user

    response = add_favorite(request, "EUR")

    self.assertEqual(response.status_code, 302)
    self.assertTrue(
        FavouriteCurrency.objects.filter(user=self.user, currency=self.eur).exists()
    )


def test_remove_favorite_view(self):
    request = RequestFactory().get(reverse("currencies:remove_favorite", args=["USD"]))
    request.user = self.user

    response = remove_favorite(request, "USD")

    self.assertEqual(response.status_code, 302)
    self.assertFalse(
        FavouriteCurrency.objects.filter(user=self.user, currency=self.usd).exists()
    )
