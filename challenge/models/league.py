from django.db import models
from challenge.models.tournament import Tournament
from team.models import Team


class League(models.Model):
    tournament_name = models.CharField(max_length=512)

    start_time = models.DateTimeField()
    match_map = models.ForeignKey('challenge.Map', related_name='leagues',
                                  on_delete=models.DO_NOTHING)
    total_matches = models.PositiveIntegerField(default=0)
    run = models.BooleanField(default=False)
    two_way = models.BooleanField(default=False)

    def pre_save(self):

        if not self.id:
            queryset = Team.humans.filter(is_finalist=False)

            teams = [team for team in queryset if team.has_final_submission()]
            print(len(teams), '*****', flush=True)
            tournament = Tournament.create_tournament(
                name=self.tournament_name,
                start_time=self.start_time,
                end_time=None,
                is_hidden=False,
                team_list=teams
            )

        if self.run:
            tournament = Tournament.objects.get(name=self.tournament_name)
            self.total_matches = tournament.make_league_for_tournament(
                match_map=self.match_map,
                two_way=self.two_way
            )

    def save(self, *args, **kwargs):
        self.pre_save()
        super().save(*args, **kwargs)
