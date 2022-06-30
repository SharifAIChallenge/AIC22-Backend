from rest_framework import serializers

from ...challenge.models.clan import Clan


class ClanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clan
        fields = (
            'name', 'leader', 'image', 'score', 'wins', 'losses', 'draws'
        )
