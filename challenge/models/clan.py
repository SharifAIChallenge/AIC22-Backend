from django.db import models
from model_utils.models import TimeStampedModel
from django.conf import settings
from constants import MEDIUM_TEXT_MAX_LENGTH


class Clan(TimeStampedModel):
    name = models.CharField(max_length=MEDIUM_TEXT_MAX_LENGTH, unique=True)
    leader = models.OneToOneField(to='team.Team', on_delete=models.PROTECT, related_name='owned_clan')
    image = models.ImageField(upload_to=settings.UPLOAD_PATHS['CLAN_IMAGE'], null=True, blank=True)  # TODO: check upload path
    score = models.PositiveIntegerField(default=0)
    wins = models.PositiveIntegerField(default=0)
    losses = models.PositiveIntegerField(default=0)
    draws = models.PositiveIntegerField(default=0)
