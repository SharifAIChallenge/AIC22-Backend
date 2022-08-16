from django.core.management import BaseCommand
from challenge.models.tournament import Tournament
from challenge.models.scoreboard import Scoreboard
from team.models import Team
from datetime import datetime
import pytz


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        tournament = Tournament.objects.all().order_by('-id').first()
        if tournament.start_time > datetime.now().replace(tzinfo=pytz.UTC):
            tournament_teams = tournament.teams()
            total_teams = [team for team in Team.humans.all() if team.has_final_submission()]
            for team in total_teams:
                if team not in tournament_teams:
                    tournament.scoreboard.add_scoreboard_row(
                        team=team
                    )
