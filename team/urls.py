from routers import CustomRouter
from .views import TeamAPIView, TeamSearchAPIView, TeamInfoAPIView, IncompleteTeamInfoListAPIView,\
    UserReceivedPendingInvitationListAPIView, UserReceivedResolvedInvitationListAPIView,\
    TeamPendingInvitationListAPIView, UserAnswerInvitationAPIView, TeamAnswerInvitationAPIView,\
    TeamSentInvitationListAPIView, UserSentInvitationListAPIView

website_router = CustomRouter()

website_router.register(r'team', TeamAPIView, basename='team_api')
website_router.register(r'team/search', TeamSearchAPIView, basename='team_search_api')
website_router.register(r'team/<int:team_id>', TeamInfoAPIView, basename='team_info_api')
website_router.register(r'team/incomplete', IncompleteTeamInfoListAPIView, basename='incomplete_team_api')
website_router.register(r'team/invitations/user_pending', UserReceivedPendingInvitationListAPIView,
                        basename='user_pending_invite_api')
website_router.register(r'team/invitations/user_resolved', UserReceivedResolvedInvitationListAPIView,
                        basename='user_resolved_invite_api')
website_router.register(r'team/invitations/team_pending', TeamPendingInvitationListAPIView,
                        basename='team_pending_invite_api')
website_router.register(r'team/invitations/user_pending/<int:invitation_id>',
                        UserAnswerInvitationAPIView, basename='user_answer_invitation_api')
website_router.register(r'team/invitations/team_pending/<str:invitation_id>',
                        TeamAnswerInvitationAPIView, basename='team_answer_invitation_api')
website_router.register(r'team/invitations/team_sent', TeamSentInvitationListAPIView,
                        basename='team_sent_invitation_api')
website_router.register(r'team/invitations/user_sent', UserSentInvitationListAPIView,
                        basename='user_sent_invitation_api')

