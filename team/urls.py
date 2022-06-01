from django.urls import path
from .views import TeamAPIView, TeamSearchAPIView, TeamInfoAPIView, IncompleteTeamInfoListAPIView,\
    UserReceivedPendingInvitationListAPIView, UserReceivedResolvedInvitationListAPIView,\
    TeamPendingInvitationListAPIView, UserAnswerInvitationAPIView, TeamAnswerInvitationAPIView,\
    TeamSentInvitationListAPIView, UserSentInvitationListAPIView

urlpatterns = [
    path('', view=TeamAPIView.as_view(), name="team_api"),
    path('search', view=TeamSearchAPIView.as_view(), name="team_search_api"),
    path('<int:team_id>', view=TeamInfoAPIView.as_view(), name="team_info_api"),
    path('incomplete', view=IncompleteTeamInfoListAPIView.as_view(), name="incomplete_team_api"),
    path('invitations/user_pending', view=UserReceivedPendingInvitationListAPIView.as_view(),
         name="user_pending_invite_api"),
    path('invitations/user_resolved', view=UserReceivedResolvedInvitationListAPIView.as_view(),
         name="user_resolved_invite_api"),
    path('invitations/team_pending', view=TeamPendingInvitationListAPIView.as_view(), name="team_pending_invite_api"),
    path('invitations/user_pending/<int:invitation_id>', view=UserAnswerInvitationAPIView.as_view(),
         name="user_answer_invitation_api"),
    path('invitations/team_pending/<str:invitation_id>', view=TeamAnswerInvitationAPIView.as_view(),
         name="team_answer_invitation_api"),
    path('invitations/team_sent', view=TeamSentInvitationListAPIView.as_view(), name="team_sent_invitation_api"),
    path('invitations/user_sent', view=UserSentInvitationListAPIView.as_view(), name="user_sent_invitation_api"),

]
