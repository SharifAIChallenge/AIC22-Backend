from django.db import models


class ClanTeam(models.Model):
    clan = models.ForeignKey(to='challenge.Clan', on_delete=models.CASCADE, name='teams')
    team = models.OneToOneField(to='team.Team', on_delete=models.PROTECT, name='clan')  # TODO: on_delete field PROTECT??!!
