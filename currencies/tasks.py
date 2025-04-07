from celery import shared_task
from currencies.fetch_rates import Command


@shared_task
def fetch_exchange_rates():
    Command().handle()
