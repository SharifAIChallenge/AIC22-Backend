from django.urls import path

from infra_gateway.views import InfraCheckGameAPIView, InfraEventPushAPIView

app_name = 'infra_gateway'

urlpatterns = [
    path(
        'event/push',
        view=InfraEventPushAPIView.as_view(),
        name="update submission"
    ),
    path(
        'game',
        view=InfraCheckGameAPIView.as_view(),
        name="check game"
    ),
]
