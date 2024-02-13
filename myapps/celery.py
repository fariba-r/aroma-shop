import os
from celery.app.base import Celery
# set the default Django settings module for the 'celery' program.
os.environ.setdefault ('DJANGO_SETTINGS_MODULE', 'aroma-shop.config.settings')

app = Celery('member')

# Using a string here means the worker doesn't
# child processes. - namespace='CELERY' means all
# celery-related configuration keys should
# have a `CELERY_` prefix.
app.config_from_object('django.conf:settings',namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
