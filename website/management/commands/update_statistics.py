

from django.core.management import BaseCommand

from django.apps import apps
from website.models import Statistic


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        for statistic in Statistic.objects.all():
            if statistic.model is None:
                continue
            model = apps.get_model(app_label=statistic.app_name, model_name=statistic.model)
            model_counter = model.objects.count()
            statistic.value = model_counter
            statistic.save()

