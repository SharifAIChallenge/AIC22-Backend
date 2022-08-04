from django.urls import path
from .views import (SubmissionsListAPIView, SubmissionAPIView, TournamentAPIView, MatchAPIView,
                    LobbyAPIView, RequestAPIView, RequestListAPIView, LevelBasedTournamentAPIView,
                    LevelBasedTournamentAddTeamsAPIView, ScoreboardAPIView, FriendlyScoreboardAPIView)

urlpatterns = [
    path('submission', view=SubmissionAPIView.as_view(), name='submission_api'),
    path('submissions', view=SubmissionsListAPIView.as_view(), name='submissions_list_api'),
    path('submission/<int:submission_id>', view=SubmissionAPIView.as_view(), name='update_submission'),
    path('tournament', view=TournamentAPIView.as_view(), name='tournament'),
    path('match', view=MatchAPIView.as_view(), name='matches'),
    path('lobby', view=LobbyAPIView.as_view(), name='lobby'),
    path('request', view=RequestListAPIView.as_view(), name='request_list'),
    path('request/<int:request_id>', view=RequestAPIView.as_view(), name='request'),
    # path('clan', view=ClanAPIView.as_view(), name='clan'),
    path('match', view=MatchAPIView.as_view(), name='matches'),
    path('level_based_tournament', view=LevelBasedTournamentAPIView.as_view(), name='level_based_tournament'),
    path(
        'level_based_tournament/add_teams',
        view=LevelBasedTournamentAddTeamsAPIView.as_view(),
        name='level_based_tournament_add_teams'
    ),
    path('scoreboard/<int:tournament_id>', view=ScoreboardAPIView.as_view(), name='scoreboard'),
    path('friendly_scoreboard', view=FriendlyScoreboardAPIView.as_view(), name='friendly_scoreboard'),
]
