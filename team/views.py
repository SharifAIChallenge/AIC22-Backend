from django.shortcuts import get_object_or_404

from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from rest_framework import status

from .serializers import TeamSerializer, TeamInfoSerializer, UserReceivedInvitationSerializer, \
    TeamPendingInvitationSerializer, TeamToUserInvitationSerializer, UserToTeamInvitationSerializer
from .models import Team, Invitation, InvitationStatusTypes, InvitationTypes
from .permissions import HasTeam, NoTeam
from account.permissions import ProfileComplete


class TeamAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TeamSerializer
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    queryset = Team.objects.all()

    def get(self, request):
        team = request.user.team
        data = self.get_serializer(team).data
        return Response(data)

    def post(self, request):
        team = self.get_serializer(data=request.data)
        team.is_valid(raise_exception=True)
        team.save()
        request.user.reject_all_pending_invites()

        return Response(
            data={"data": team.data},
            status=status.HTTP_200_OK
        )

    def put(self, request):
        team = self.get_serializer(data=request.data,
                                   instance=request.user.team, partial=True)
        team.is_valid(raise_exception=True)
        team.save()

        return Response(
            data={"data": team.data},
            status=status.HTTP_200_OK
        )

    def delete(self, request):
        current_user = request.user

        if current_user.team.member_count() == 1 and current_user.team.creator is current_user:
            current_user.team.delete()
        current_user.team = None
        current_user.save()

        return Response(
            data={"message": "You left the team"},
            status=status.HTTP_200_OK
        )

    def get_permissions(self):
        new_permissions = self.permission_classes.copy()
        if self.request.method in ['PUT', 'GET', 'DELETE']:
            new_permissions += [HasTeam]
        if self.request.method == 'POST':
            new_permissions += [NoTeam, ProfileComplete]
        return [permission() for permission in new_permissions]


class TeamSearchAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = TeamSerializer
    queryset = Team.objects.all()

    def get(self, request):
        term = request.GET.get('search')
        if term is None or term == '':
            return Response(data={"message": "Provide search parameter"},
                            status=status.HTTP_400_BAD_REQUEST)
        teams = self.get_queryset().filter(name__icontains=term)
        page = self.paginate_queryset(teams)
        results = self.get_serializer( page, many=True)

        return self.get_paginated_response(
            data={"data": results.data}
        )


class TeamInfoAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TeamInfoSerializer
    queryset = Team.objects.all()
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def get(self, request, team_id):
        team = get_object_or_404(Team, id=team_id)
        data = self.get_serializer(instance=team).data

        return Response(
            data={'data': data},
            status=status.HTTP_200_OK
        )


class IncompleteTeamInfoListAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = TeamInfoSerializer
    queryset = Team.objects.all()
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request):
        incomplete_teams_id = [team.id for team in
                               filter(lambda team: not team.is_complete(), self.get_queryset())]
        incomplete_teams = self.get_queryset().filter(id__in=incomplete_teams_id)
        page = self.paginate_queryset(incomplete_teams)
        data = self.get_serializer(instance=page, many=True).data

        return self.get_paginated_response(data={'data': data})

    def get_queryset(self):
        name = self.request.query_params.get('name')
        queryset = Team.objects.all()

        if name:
            queryset = queryset.filter(name__icontains=name)

        return queryset


class UserReceivedPendingInvitationListAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = UserReceivedInvitationSerializer
    queryset = Invitation.objects.all()

    def get(self, request):
        invitations = self.get_queryset().filter(user=request.user,
                                                 status=InvitationStatusTypes.PENDING,
                                                 type=InvitationTypes.TEAM_TO_USER)
        data = self.get_serializer(instance=invitations, many=True).data
        return Response(
            data={'data': data},
            status=status.HTTP_200_OK
        )


class UserReceivedResolvedInvitationListAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = UserReceivedInvitationSerializer
    queryset = Invitation.objects.all()

    def get(self, request):
        invitations = self.get_queryset().filter(user=request.user,
                                                 type=InvitationTypes.TEAM_TO_USER).\
            exclude(status=InvitationStatusTypes.PENDING)
        data = self.get_serializer(instance=invitations, many=True).data

        return Response(
            data={'data': data},
            status=status.HTTP_200_OK
        )


class TeamPendingInvitationListAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated, HasTeam]
    serializer_class = TeamPendingInvitationSerializer
    queryset = Invitation.objects.all()

    def get(self, request):
        invitations = self.get_queryset().filter(team=request.user.team,
                                                 status=InvitationStatusTypes.PENDING,
                                                 type=InvitationTypes.USER_TO_TEAM)
        data = self.get_serializer(instance=invitations, many=True).data

        return Response(
            data={'data': data},
            status=status.HTTP_200_OK
        )


class UserAnswerInvitationAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated, NoTeam]
    serializer_class = UserReceivedInvitationSerializer
    queryset = Invitation.objects.all()

    def put(self, request, invitation_id):
        invitation = get_object_or_404(Invitation, id=invitation_id)
        serializer = self.get_serializer(instance=invitation,
                                         data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        if request.query_params.get('answer') == 'yes':
            user = invitation.user
            user.team = invitation.team
            invitation.save()
            user.save()
            if invitation.team.is_complete():
                invitation.team.reject_all_pending_invitations()
            user.reject_all_pending_invites()

        return Response(
            data={"detail": f"Invitation is {serializer.data['status']}"},
            status=status.HTTP_200_OK
        )

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['invitation_id'] = self.kwargs['invitation_id']
        return context


class TeamAnswerInvitationAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated, HasTeam]
    serializer_class = TeamPendingInvitationSerializer
    queryset = Invitation.objects.all()

    def put(self, request, invitation_id):
        invitation = get_object_or_404(Invitation, id=invitation_id)
        serializer = self.get_serializer(instance=invitation,
                                         data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        if request.query_params.get('answer') == 'yes':
            user = invitation.user
            user.team = invitation.team
            user.save()
            if invitation.team.is_complete():
                invitation.team.reject_all_pending_invitations()
            user.reject_all_pending_invites()

        return Response(
            data={"detail": f"Invitation is {serializer.data['status']}"},
            status=status.HTTP_200_OK
        )

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['invitation_id'] = self.kwargs['invitation_id']
        return context


class TeamSentInvitationListAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated, HasTeam, ]
    serializer_class = TeamToUserInvitationSerializer
    queryset = Invitation.objects.all()

    def get(self, request):
        invitations = self.get_queryset().filter(team=request.user.team,
                                                 type=InvitationTypes.TEAM_TO_USER)
        data = self.get_serializer(instance=invitations, many=True).data

        return Response(
            data={'data': data},
            status=status.HTTP_200_OK
        )

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            data={"message": "your invitation sent"},
            status=status.HTTP_200_OK
        )


class UserSentInvitationListAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated, NoTeam]
    serializer_class = UserToTeamInvitationSerializer
    queryset = Invitation.objects.all()

    def get(self, request):
        invitations = self.get_queryset().filter(user=request.user,
                                                 type=InvitationTypes.USER_TO_TEAM)
        data = self.get_serializer(instance=invitations, many=True).data
        return Response(
            data={'data': data},
            status=status.HTTP_200_OK
        )

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            data={"message": "your invitation sent"},
            status=status.HTTP_200_OK
        )
