import os

from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CurrencyExchange.settings')

app = Celery('CurrencyExchange')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


app.conf.beat_schedule = {
    'fetch-daily-rates': {
        'task': 'currencies.tasks.fetch_exchange_rates',
        # 'schedule': crontab(minute='*'), # every minute
        # 'schedule': crontab(hour='*', minute='0'), # every hour
        'schedule': crontab(hour='16', minute='0'),  # every day at 16:00 UTC
    },
}
