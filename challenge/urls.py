from django.urls import path
from .views import SubmissionsListAPIView, SubmissionAPIView, TournamentAPIView, MatchAPIView

urlpatterns = [
    path('submission', view=SubmissionAPIView.as_view(), name='submission_api'),
    path('submissions', view=SubmissionsListAPIView.as_view(),
         name='submissions_list_api'),
    path('tournament', view=TournamentAPIView.as_view(), name='tournament'),
    path('match', view=MatchAPIView.as_view(), name='matches'),
]
