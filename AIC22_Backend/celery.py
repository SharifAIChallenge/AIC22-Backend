from __future__ import absolute_import, unicode_literals
import os

from AIC22_Backend import settings
from celery import Celery

""" RabbitMQ as message broker
"""

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AIC22_Backend.settings')
app = Celery(main='AIC22_Backend', broker=settings.RABBITMQ_BROKER)
app.config_from_object('django.conf:settings')

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
