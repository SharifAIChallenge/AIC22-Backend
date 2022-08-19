from django.db import models
from model_utils.models import TimeStampedModel
from team.models import Team
from challenge.models.scoreboard import Scoreboard
from constants import SHORT_TEXT_MAX_LENGTH, LONG_TEXT_MAX_LENGTH


class TournamentTypes:
    NORMAL = 'normal'
    FRIENDLY = 'friendly'
    CLANWAR = 'clanwar'
    BOT = 'bot'
    FINAL = 'final'
    TYPES = (
        (NORMAL, 'Normal'),
        (FRIENDLY, 'Friendly'),
        (CLANWAR, 'Clanwar'),
        (BOT, 'Bot'),
        (FINAL, 'Final')
    )


class Tournament(TimeStampedModel):
    name = models.CharField(max_length=LONG_TEXT_MAX_LENGTH, unique=True)
    type = models.CharField(
        max_length=SHORT_TEXT_MAX_LENGTH,
        choices=TournamentTypes.TYPES,
        default=TournamentTypes.NORMAL
    )
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    is_hidden = models.BooleanField(default=False)
    priority = models.IntegerField(default=0)

    @staticmethod
    def get_friendly_tournament():
        return Tournament.objects.filter(
            type=TournamentTypes.FRIENDLY
        ).first()

    @staticmethod
    def get_bot_tournament():
        return Tournament.objects.filter(
            type=TournamentTypes.BOT
        ).first()

    def update_members(self):
        for row in self.scoreboard.rows:
            row.delete()

        queryset = Team.humans.filter(is_finalist=False)
        teams = [team for team in queryset if team.has_final_submission()]
        for team in teams:
            self.scoreboard.add_scoreboard_row(
                team=team
            )

    @staticmethod
    def create_tournament(
            name, start_time, end_time, is_hidden,
            is_friendly=False, team_list=None,
            is_scoreboard_freeze=False,
            tournament_type=TournamentTypes.NORMAL
    ):
        if team_list is None:
            team_list = []

        tournament = Tournament.objects.create(
            name=name,
            start_time=start_time,
            end_time=end_time,
            is_hidden=is_hidden,
            type=tournament_type
        )
        scoreboard = Scoreboard.objects.create(
            tournament=tournament,
            freeze=is_scoreboard_freeze
        )
        for team in team_list:
            scoreboard.add_scoreboard_row(
                team=team
            )

        return tournament

    def teams(self):
        from team.models import Team
        team_ids = self.scoreboard.rows.values_list('team_id', flat=True)

        return Team.humans.filter(id__in=team_ids)
        
    def make_league_for_tournament(self, match_map, two_way=False):  ## HERE
        from itertools import combinations

        from challenge.models.match import Match

        teams = self.teams()
        binaries = list(combinations(list(teams), 2))

        for team1, team2 in binaries:
            Match.create_match(
                team1=team1,
                team2=team2,
                tournament=self,
                match_map=match_map
            )

        if two_way:
            for team2, team1 in binaries:
                Match.create_match(
                    team1=team1,
                    team2=team2,
                    tournament=self,
                    match_map=match_map
                )
        if two_way:
            return 2 * len(binaries)

        return len(binaries)

    def make_league_multi_maps(self, match_maps, two_way=False):
        total_matches = 0

        for match_map in match_maps:
            total_matches += self.make_league_for_tournament(
                match_map=match_map,
                two_way=two_way
            )
        return total_matches

    def run_next_swiss_round(self, game_maps):
        self.__run_swiss_round(self.scoreboard, game_maps)

    def __run_swiss_round(self, scoreboard, game_maps):
        pass  # TODO

    def init_swiss_league(self, src_tournament: 'Tournament', game_maps):
        self.__run_swiss_round(src_tournament.scoreboard, game_maps)

    def __str__(self):
        return f'{self.name}'
