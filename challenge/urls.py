from django.urls import path
from .views import SubmissionsListAPIView, SubmissionAPIView

urlpatterns = [
    path('submission', view=SubmissionAPIView.as_view(), name='submission_api'),
    path('submissions', view=SubmissionsListAPIView.as_view(),
         name='submissions_list_api'),
]
