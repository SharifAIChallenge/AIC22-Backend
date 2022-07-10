from django.db import models

from model_utils.models import TimeStampedModel


class Scoreboard(TimeStampedModel):
    tournament = models.OneToOneField(
        to='challenge.Tournament',
        on_delete=models.CASCADE,
        related_name='scoreboard'
    )
    freeze = models.BooleanField(default=False)

    def add_scoreboard_row(self, team):
        if not self.rows.filter(team=team).exists():
            row = ScoreboardRow.objects.create(
                scoreboard=self,
                team=team,
            )
            return row
        return None


class ScoreboardRow(TimeStampedModel):
    scoreboard = models.ForeignKey(
        to='challenge.Scoreboard',
        on_delete=models.CASCADE,
        related_name='rows'
    )
    team = models.ForeignKey(
        to='team.Team',
        on_delete=models.CASCADE,
        related_name='scoreboard_rows'
    )
    score = models.PositiveIntegerField(default=1000)
    wins = models.PositiveIntegerField(default=0)
    losses = models.PositiveIntegerField(default=0)
    draws = models.PositiveIntegerField(default=0)
