from django.shortcuts import get_object_or_404

from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

from constants import IMAGE_MAX_SIZE
from account.serializers import ShortProfileSerializer
from utils.image_url import ImageURL
from account.serializers import ProfileSerializer
from account.models import User
from .models import Team, Invitation
from .exceptions import TeamIsFullException, DuplicatePendingInviteException, HasTeamException


class MemberSerializer(serializers.ModelSerializer):
    profile = ShortProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['email', 'profile']


class TeamSerializer(serializers.ModelSerializer, ImageURL):
    members = MemberSerializer(many=True, read_only=True)
    creator = MemberSerializer(read_only=True)

    image_url = serializers.SerializerMethodField('_image_url')

    class Meta:
        model = Team
        fields = ['name', 'image', 'members', 'creator', 'image_url', 'id', 'is_finalist', 'final_payed']

    def create(self, data):
        current_user = self.context['request'].user
        data['creator'] = current_user

        team = Team.humans.create(**data)

        current_user.team = team
        current_user.save()
        return team

    def validate(self, attrs):
        image = attrs.get('image')

        if image and image.size > IMAGE_MAX_SIZE:
            raise serializers.ValidationError('Maximum file size reached')

        return attrs


class TeamInfoSerializer(serializers.ModelSerializer, ImageURL):
    members = MemberSerializer(many=True, read_only=True)
    creator = MemberSerializer(read_only=True)
    image_url = serializers.SerializerMethodField('_image_url')

    class Meta:
        model = Team
        fields = ['name', 'image', 'creator', 'members', 'image_url', 'id', 'is_finalist', 'final_payed']


class UserToTeamInvitationSerializer(serializers.ModelSerializer):
    team = TeamInfoSerializer(read_only=True)

    class Meta:
        model = Invitation
        fields = ['team', 'status']

    def create(self, data):
        data['type'] = 'user_to_team'
        current_user = self.context['request'].user
        data['user'] = current_user
        data['team'] = get_object_or_404(Team, id=self.context['request'].data['team_id'])
        invitation = Invitation.objects.create(**data)
        return invitation

    def validate(self, data):
        request = self.context['request']
        team = get_object_or_404(Team, id=self.context['request'].data['team_id'])
        if team.is_complete():
            raise TeamIsFullException()
        elif Invitation.objects.filter(team=team, user=request.user, status='pending').exists():
            raise DuplicatePendingInviteException()
        return data


class TeamToUserInvitationSerializer(serializers.ModelSerializer):
    user = MemberSerializer(read_only=True)

    class Meta:
        model = Invitation
        fields = ['user', 'status']

    def create(self, data):
        current_user = self.context['request'].user
        data['team'] = current_user.team
        data['type'] = 'team_to_user'
        data['user'] = get_object_or_404(User,
                                         email=self.context['request'].data[
                                             'user_email'])
        invitation = Invitation.objects.create(**data)
        return invitation

    def validate(self, data):
        request = self.context['request']
        target_user = get_object_or_404(User, email=request.data['user_email'])
        if request.user.team.is_complete():
            raise TeamIsFullException()
        elif target_user.team is not None:
            raise HasTeamException()
        elif Invitation.objects.filter(team=request.user.team,
                                       user=target_user,
                                       status='pending').exists():
            raise DuplicatePendingInviteException()
        return data


class UserReceivedInvitationSerializer(serializers.ModelSerializer):
    team = TeamInfoSerializer(read_only=True)

    def validate(self, data):
        request = self.context['request']
        invitation = get_object_or_404(Invitation,
                                       id=self.context['invitation_id'])
        answer = request.query_params.get('answer', "no")

        if request.user != invitation.user:
            raise PermissionDenied('this is not your invitation to change')
        elif answer == 'yes':
            if invitation.team.is_complete():
                raise TeamIsFullException()
            data['status'] = 'accepted'
        elif answer == 'no':
            data['status'] = 'rejected'
        return data

    class Meta:
        model = Invitation
        fields = ['team', 'status', 'id']


class TeamPendingInvitationSerializer(serializers.ModelSerializer):
    user = MemberSerializer(read_only=True)

    def validate(self, data):
        request = self.context['request']
        invitation = get_object_or_404(Invitation,
                                       id=self.context['invitation_id'])

        answer = request.query_params.get('answer', 'no')
        if request.user.team != invitation.team:
            raise PermissionDenied('this is not your invitation to change')
        elif answer == 'yes':
            if invitation.team.is_complete():
                raise TeamIsFullException()
            data['status'] = 'accepted'
        elif answer == 'no':
            data['status'] = 'rejected'
        return data

    class Meta:
        model = Invitation
        fields = ['user', 'status', 'id']
