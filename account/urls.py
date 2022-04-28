from django.urls import path

from account.views import SignUpAPIView, LoginAPIView, LogoutAPIView, ActivateAPIView, ProfileAPIView

urlpatterns = [

    path('signup', view=SignUpAPIView.as_view(), name='signup'),
    path('login', view=LoginAPIView.as_view(), name='login'),
    path('logout', view=LogoutAPIView.as_view(), name='logout'),
    path('activate/<slug:eid>/<slug:token>', view=ActivateAPIView.as_view(), name='activate')
    path('profile', view=ProfileAPIView.as_view(), name='profile')
]
