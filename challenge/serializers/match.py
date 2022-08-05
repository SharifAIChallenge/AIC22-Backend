from rest_framework import serializers

from challenge.models.match import Match
from challenge.models.tournament import Tournament
from team.models import Team


class MatchTeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['name']


class MatchTournamentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tournament
        fields = ['name']


class MatchSerializer(serializers.ModelSerializer):
    team1 = MatchTeamSerializer(read_only=True)
    team2 = MatchTeamSerializer(read_only=True)
    winner = MatchTeamSerializer(read_only=True)

    class Meta:
        model = Match
        fields = ('team1', 'team2', 'status', 'winner', 'log', 'tournament')

    def to_representation(self, instance: Match):
        data = super().to_representation(instance)
        if instance.status in ['successful', 'failed']:
            data['log'] = f'https://cdn.aichallenge.ir/log/{instance.infra_token}/{instance.infra_token}.log'
        if self.context['request'].user.team.name == data['team2']['name']:
            data['team1'], data['team2'] = data['team2'], data['team1']
        # data['log'] = instance.game_log
        # data['server_log'] = instance.server_log

        return data
