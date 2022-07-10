from rest_framework import serializers

from challenge.models.scoreboard import ScoreboardRow, Scoreboard
from team.serializers import TeamInfoSerializer


class ScoreboardRowSerializer(serializers.ModelSerializer):
    team = TeamInfoSerializer(read_only=True)

    class Meta:
        model = ScoreboardRow
        fields = ('team', 'score', 'wins', 'losses', 'draws')


class ScoreboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scoreboard
        fields = ('tournament', 'freeze')
