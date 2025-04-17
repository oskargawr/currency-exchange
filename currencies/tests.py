from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from currencies.models import Currency, FavouriteCurrency, ExchangeRate


class CurrencyTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        FavouriteCurrency.objects.all().delete()
        ExchangeRate.objects.all().delete()
        Currency.objects.all().delete()
        User.objects.filter(username__in=["testuser", "admin"]).delete()
        cls.user = User.objects.create_user(username="testuser", password="password")
        cls.usd, _ = Currency.objects.get_or_create(
            base="USD", defaults={"name": "US Dollar", "symbol": "$"}
        )
        ExchangeRate.objects.update_or_create(
            currency=cls.usd, date="2023-01-01", rate=1.0
        )
        FavouriteCurrency.objects.update_or_create(user=cls.user, currency=cls.usd)

    def setUp(self):
        self.client = Client()
        self.client.force_login(self.user)

    def test_currency_list_view(self):
        response = self.client.get(reverse("currencies:currency_list"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("page_obj", response.context)

    def test_currency_detail_view(self):
        response = self.client.get(reverse("currencies:detail", args=["USD"]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["currency"].base, "USD")

    def test_favorite_currencies_view(self):
        response = self.client.get(reverse("currencies:favorites"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["favorites"]), 1)

    def test_add_favorite_view(self):
        eur = Currency.objects.create(base="EUR", name="Euro", symbol="€")
        response = self.client.get(reverse("currencies:add_favorite", args=["EUR"]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            FavouriteCurrency.objects.filter(user=self.user, currency=eur).exists()
        )

    def test_remove_favorite_view(self):
        response = self.client.get(reverse("currencies:remove_favorite", args=["USD"]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            FavouriteCurrency.objects.filter(user=self.user, currency=self.usd).exists()
        )
