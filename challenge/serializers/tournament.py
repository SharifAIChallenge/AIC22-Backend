from rest_framework import serializers

from challenge.models.tournament import Tournament


class TournamentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tournament
        fields = ('id', 'name', 'type', 'start_time', 'end_time')

    def to_representation(self, instance: Tournament):
        data = super().to_representation(instance)
        teams = instance.teams()
        data['participants'] = len(teams)
        data['is_member'] = self.context['request'].user.team in teams

        return data


class LevelBasedTournamentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tournament
        fields = ('name', 'start_time', 'end_time', 'is_hidden')
        # 'is_friendly', 'is_scoreboard_freeze')
