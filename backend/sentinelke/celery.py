from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sentinelke.settings')

app = Celery('sentinelke')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
