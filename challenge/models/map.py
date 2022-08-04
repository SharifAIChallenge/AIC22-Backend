from django.db import models
from model_utils.models import TimeStampedModel, UUIDModel
from django.conf import settings

from constants import LONG_TEXT_MAX_LENGTH


class Map(TimeStampedModel, UUIDModel):
    name = models.CharField(
        max_length=LONG_TEXT_MAX_LENGTH,
        unique=True
    )
    file = models.FileField(
        upload_to=settings.UPLOAD_PATHS["MAP"]
    )
    active = models.BooleanField(default=True)
    infra_token = models.CharField(
        max_length=LONG_TEXT_MAX_LENGTH,
        blank=True,
        null=True
    )

    def pre_save(self):
        from challenge.logics import upload_map
        self.infra_token = upload_map(self.file)

    def save(self, *args, **kwargs):
        self.pre_save()
        super().save(*args, **kwargs)

    @staticmethod
    def get_random_map():
        game_map = Map.objects.filter(active=True).order_by('?').first()
        if game_map is None:
            raise Exception("There is no map available in the database")

        return game_map

    def __str__(self):
        return f'{self.name}'
