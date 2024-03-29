from django.shortcuts import get_object_or_404
from rest_framework import serializers

from challenge.exceptions import SelfRequestException, NoFinalSubmission, DuplicatePendingRequestException
from challenge.models.request import Request
from team.models import Team


class RequestSerializer(serializers.ModelSerializer):
    source_team_name = serializers.SerializerMethodField('_source_team_name')
    target_team_name = serializers.SerializerMethodField('_target_team_name')

    @staticmethod
    def _source_team_name(obj: Request):
        return obj.source_team.name

    @staticmethod
    def _target_team_name(obj: Request):
        return obj.target_team.name

    class Meta:
        model = Request
        fields = ('id', 'source_team', 'target_team', 'status', 'type',
                  'source_team_name', 'target_team_name')
        read_only_fields = ('source_team', 'status', 'source_team_name',
                            'target_team_name')

    def create(self, validated_data):
        validated_data['source_team'] = self.context['request'].user.team

        return Request.objects.create(**validated_data)

    def validate(self, data):
        request = self.context['request']
        target_team = get_object_or_404(Team, id=request.data['target_team'])
        if not target_team.has_final_submission():
            raise NoFinalSubmission()
        if target_team == request.user.team:
            raise SelfRequestException()
        elif Request.objects.filter(
                target_team=target_team,
                source_team=request.user.team,
                status='pending'
        ).exists():
            raise DuplicatePendingRequestException()
        return data
