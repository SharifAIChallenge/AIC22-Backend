from rest_framework import serializers

from challenge.models.level_match import LevelMatch


class LevelMatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = LevelMatch
        fields = ('match', 'level')
