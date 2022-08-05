from rest_framework import serializers

from challenge.models.map import Map


class MapSerializer(serializers.ModelSerializer):
    class Meta:
        model = Map
        fields = ('id', 'name', 'active', 'file', 'config_file')
