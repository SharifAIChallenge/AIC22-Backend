from django.urls import path

from account.views import SignUpAPIView, LoginAPIView, LogoutAPIView, ActivateAPIView, ProfileAPIView, \
    GoogleLoginAPIView, ChangePasswordAPIView, ResendActivationEmailAPIView, ResetPasswordAPIView, \
    ResetPasswordConfirmAPIView, UserWithoutTeamAPIView, CustomLoginAPIView

urlpatterns = [

    path('signup', view=SignUpAPIView.as_view(), name='signup'),
    path('login', view=CustomLoginAPIView.as_view(), name='login'),
    path('logout', view=LogoutAPIView.as_view(), name='logout'),
    path('activate/<slug:eid>/<slug:token>', view=ActivateAPIView.as_view(), name='activate'),
    path('profile', view=ProfileAPIView.as_view(), name='profile'),
    path('social-login', view=GoogleLoginAPIView.as_view(), name='social_login'),
    path('password/change', ChangePasswordAPIView.as_view()),
    path('resend-activation-link', view=ResendActivationEmailAPIView.as_view(), name='resend'),
    path('password/reset', view=ResetPasswordAPIView.as_view(), name='reset password'),
    path('password/reset/confirm', view=ResetPasswordConfirmAPIView.as_view(), name='confirm password'),
    path('without_team', view=UserWithoutTeamAPIView.as_view(), name='users without team'),
]
