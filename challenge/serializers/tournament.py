from rest_framework import serializers

from challenge.models.tournament import Tournament


class TournamentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tournament
        fields = ('id', 'name', 'type', 'start_time', 'end_time')
