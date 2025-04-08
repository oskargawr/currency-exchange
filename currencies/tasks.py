from celery import shared_task
from currencies.management.commands.fetch_rates import Command


@shared_task
def fetch_exchange_rates():
    Command().handle()
