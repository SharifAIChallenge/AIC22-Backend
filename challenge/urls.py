from django.urls import path
from .views import (SubmissionsListAPIView, SubmissionAPIView, TournamentAPIView, MatchAPIView,
                    LobbyAPIView, RequestAPIView, RequestListAPIView)
urlpatterns = [
    path('submission', view=SubmissionAPIView.as_view(), name='submission_api'),
    path('submissions', view=SubmissionsListAPIView.as_view(),
         name='submissions_list_api'),
    path('tournament', view=TournamentAPIView.as_view(), name='tournament'),
    path('match', view=MatchAPIView.as_view(), name='matches'),
    path('lobby', view=LobbyAPIView.as_view(), name='lobby'),
    path('request', view=RequestListAPIView.as_view(), name='request_list'),
    path('request/<int:request_id>', view=RequestAPIView.as_view(), name='request'),
]
