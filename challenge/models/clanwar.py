from django.db import models
from model_utils.models import TimeStampedModel


class ClanWar(TimeStampedModel):
    clan1 = models.ForeignKey(to='challenge.Clan', on_delete=models.PROTECT, related_name='clanwars1')
    clan2 = models.ForeignKey(to='challenge.Clan', on_delete=models.PROTECT, related_name='clanwars2')
    tournament = models.OneToOneField(to='challenge.Tournament', on_delete=models.CASCADE, related_name='clanwar')

    @property
    def winner(self):
        return None  # TODO: complete this method
