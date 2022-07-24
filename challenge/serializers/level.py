from rest_framework import serializers

from challenge.models.level import Level


class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = ('number', 'level_based_tournament')
