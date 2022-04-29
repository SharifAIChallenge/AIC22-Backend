from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _
from account.models import Profile, User
from account.serializers import UserSerializer, EmailSerializer


class SignUpAPIView(GenericAPIView):
    queryset = Profile.objects.all()
    serializer_class = UserSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user.send_activation_email()

        return Response(
            data={'detail': _('Check your email for confirmation link')},
            status=200
        )


LoginAPIView = ObtainAuthToken


class LogoutAPIView(GenericAPIView):
    queryset = Profile.objects.all()
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


class ActivateAPIView(GenericAPIView):

    def get(self, request, eid, token):
        User.activate(eid, token)
        return Response(data={'detail': _('Account Activated')},
                        status=status.HTTP_200_OK)


class ResendActivationEmailAPIView(GenericAPIView):
    serializer_class = EmailSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = get_object_or_404(User,
                                     email=serializer.validated_data['email'])
            user.send_activation_email()
            return Response(
                data={'detail': _('Check your email for confirmation link')},
                status=200
            )
