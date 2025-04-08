from datetime import date

from django.core.management import BaseCommand
import requests

from CurrencyExchange import settings
from currencies.models import ExchangeRate, Currency


class Command(BaseCommand):
    help = 'fetching latest exchange rates from ExchangeRate-API'

    def handle(self, *args, **options):
        url = f"{settings.EXCHANGERATE_API_URL}{settings.EXCHANGE_RATE_API_KEY}/latest/USD"

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            if data['result'] == 'success':
                today = date.today()
                rates = data['conversion_rates']

                for currency_code, rate in rates.items():
                    if currency_code == 'USD':
                        continue

                    currency, created = Currency.objects.get_or_create(
                        base=currency_code,
                        defaults={'name': currency_code}
                    )

                    ExchangeRate.objects.get_or_create(
                        currency=currency,
                        date=today,
                        defaults={'rate': rate}
                    )

                self.stdout.write(self.style.SUCCESS(f'Successfully fetched rates for {len(rates) - 1} currencies'))
            else:
                self.stdout.write(self.style.ERROR(f'API error: {data["error-type"]}'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error fetching rates: {str(e)}'))
