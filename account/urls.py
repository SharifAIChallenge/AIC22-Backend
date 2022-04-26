from django.urls import path

from account.views import SignUpAPIView
from routers import CustomRouter

urlpatterns = [

    path('signup', view=SignUpAPIView.as_view(), name='signup')
]