from django.conf import settings
from django.db import models
from model_utils.models import TimeStampedModel
from rest_framework.generics import get_object_or_404

from constants import SHORT_TEXT_MAX_LENGTH, LONG_TEXT_MAX_LENGTH


class MatchStatusTypes:
    FREEZE = 'freeze'
    PENDING = 'pending'
    FAILED = 'failed'
    SUCCESSFUL = 'successful'
    RUNNING = 'running'
    TYPES = (
        (FAILED, 'Failed'),
        (SUCCESSFUL, 'Successful'),
        (RUNNING, 'Running'),
        (FREEZE, 'Freeze'),
        (PENDING, 'pending')
    )


class Match(TimeStampedModel):
    team1 = models.ForeignKey(to='team.Team', on_delete=models.CASCADE,
                              related_name='matches_first')
    team2 = models.ForeignKey(to='team.Team', on_delete=models.CASCADE,
                              related_name='matches_second')
    status = models.CharField(
        max_length=SHORT_TEXT_MAX_LENGTH,
        choices=MatchStatusTypes.TYPES,
        default=MatchStatusTypes.FREEZE
    )
    winner = models.ForeignKey(to='team.Team', on_delete=models.CASCADE,
                               related_name='won_matches', null=True,
                               blank=True)
    log = models.FileField(upload_to=settings.UPLOAD_PATHS['MATCH_LOGS'],
                           null=True, blank=True)
    log_file_token = models.CharField(max_length=LONG_TEXT_MAX_LENGTH, null=True, blank=True)
    tournament = models.ForeignKey(
        to='challenge.Tournament',
        on_delete=models.CASCADE,
        related_name='matches'
    )

    infra_token = models.CharField(
        max_length=LONG_TEXT_MAX_LENGTH,
        blank=True,
        null=True
    )

    @property
    def is_freeze(self):
        return self.status == MatchStatusTypes.FREEZE

    @property
    def is_successful(self):
        return self.status == MatchStatusTypes.SUCCESSFUL

    @classmethod
    def update_match(cls, infra_token, status, message=None, stats=None):
        match: 'Match' = get_object_or_404(
            cls, infra_token=infra_token
        )

        if message:
            match.message = message

        if stats and not match.winner:
            winner = stats.get('winner', 0)
            if winner == 0:
                match.winner = match.team1
            elif winner == 1:
                match.winner = match.team2

            match.update_score()

        match.status = status
        match.save()

        return match

    def run_match(self, priority=0):
        # from apps.infra_gateway.functions import run_match
        # self.infra_token = run_match(
        #     match=self,
        #     priority=priority
        # )
        # self.save()
        pass # TODO


    @staticmethod
    def run_matches(matches, priority=0):
        for match in matches:
            match.run_match(priority=priority)

    @staticmethod
    def create_match(team1, team2, tournament, match_map, is_freeze=False,
                     priority=0):
        from challenge.models.match_info import MatchInfo

        team1_final_submission = team1.final_submission()
        team2_final_submission = team2.final_submission()

        if team1_final_submission and team2_final_submission:
            match = Match.objects.create(
                team1=team1,
                team2=team2,
                status=MatchStatusTypes.PENDING
                if not is_freeze else MatchStatusTypes.FREEZE,
                tournament=tournament
            )
            match_info = MatchInfo.objects.create(
                team1_code=team1_final_submission,
                team2_code=team2_final_submission,
                match=match,
                map=match_map
            )

            if not is_freeze:
                match.run_match(priority=priority)

            return match
        return None

    @staticmethod
    def create_friendly_match(team1, team2, game_map=None):
        from challenge.models.map import Map
        from challenge.models.tournament import Tournament

        if game_map is None:
            game_map = Map.get_random_map()
        friendly_tournament = Tournament.get_friendly_tournament()

        if friendly_tournament is None:
            raise Exception(
                "Admin should initialize a friendly tournament first ...")

        return Match.create_match(team1, team2, friendly_tournament, game_map,
                                  priority=1)

    @staticmethod
    def create_bot_match(bot, team, game_map=None):
        from challenge.models.map import Map
        from challenge.models.tournament import Tournament

        if game_map is None:
            game_map = Map.get_random_map()
        bot_tournament = Tournament.get_bot_tournament()

        if bot_tournament is None:
            raise Exception(
                "Admin should initialize a bot tournament first ..."
            )

        return Match.create_match(bot, team, bot_tournament, game_map,
                                  priority=1)
