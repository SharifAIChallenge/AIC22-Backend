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

    def get_team_row(self, team):
        row = self.rows.filter(team=team).last()
        if not row:
            row = ScoreboardRow.objects.create(scoreboard=self, team=team)

        return row

    @staticmethod
    def merge_scoreboards(src: 'Scoreboard', dest: 'Scoreboard',
                          cost=1000, coef=1):
        for row in src.rows.all():
            dest_row = dest.rows.filter(team_id=row.team_id).last()
            if not dest_row:
                continue
            dest_row.wins += row.wins
            dest_row.losses += row.losses
            dest_row.draws += row.draws
            dest_row.score += (row.score - cost) * coef
            dest_row.save()

    def __str__(self):
        return f'{self.tournament.name}'


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
