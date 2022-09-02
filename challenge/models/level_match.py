from django.db import models
from model_utils.models import TimeStampedModel


class LevelMatch(TimeStampedModel):
    match = models.OneToOneField(
        to='challenge.Match',
        on_delete=models.PROTECT,
        related_name='level_match'
    )
    level = models.ForeignKey(
        to='challenge.Level',
        on_delete=models.CASCADE,
        related_name='level_matches'
    )

    @staticmethod
    def create_level_matches(match_list, level):
        level_matches = []

        for match in match_list:
            level_match = LevelMatch.objects.create(
                match=match,
                level=level
            )
            level_matches.append(level_match)

        return level_matches

    @staticmethod
    def get_winners_from_3_matchs(level):
        matchs = LevelMatch.objects.filter(level=level)
        teams = {}
        for match in matchs:
            if match.match.winner.name in teams:
                teams[match.match.winner.name] += 1
            else:
                teams[match.match.winner.name] = 1
        return teams
