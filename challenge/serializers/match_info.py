from rest_framework import serializers

from challenge.models.match_info import MatchInfo


class MatchInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MatchInfo
        fields = ('team1_score', 'team2_score', 'match_duration', 'map')
