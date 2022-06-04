from django.contrib.auth.hashers import make_password
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.http import urlsafe_base64_decode
from rest_framework import status, serializers, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import GenericAPIView
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _
from account.models import Profile, User, ResetPasswordToken
from account.serializers import UserSerializer, EmailSerializer, ProfileSerializer, GoogleLoginSerializer, \
    ChangePasswordSerializer, ResetPasswordConfirmSerializer


class GoogleLoginAPIView(GenericAPIView):
    serializer_class = GoogleLoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.save()

        return Response(
            data={'token': token.key},
            status=status.HTTP_200_OK
        )


class SignUpAPIView(GenericAPIView):
    queryset = Profile.objects.all()
    serializer_class = UserSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            with transaction.atomic():
                user = serializer.save()
                user.send_activation_email()
        except Exception as e:
            print(e)
            # TODO: logger.error
            return Response(
                data={'detail': _('An error occurred. Please try again later.')},
                status=500
            )

        return Response(
            data={'detail': _('Check your email for confirmation link')},
            status=200
        )


LoginAPIView = ObtainAuthToken


class LogoutAPIView(GenericAPIView):
    queryset = Profile.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.Serializer

    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


class ActivateAPIView(GenericAPIView):
    serializer_class = serializers.Serializer

    def get(self, request, eid, token):
        User.activate(eid, token)
        return Response(data={'detail': _('Account Activated')},
                        status=status.HTTP_200_OK)


class ChangePasswordAPIView(GenericAPIView):
    queryset = User.objects.all()
    serializer_class = ChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            data={'detail': _('password changed successfully')},
            status=200
        )


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


class ResetPasswordAPIView(GenericAPIView):
    serializer_class = EmailSerializer

    def post(self, request):
        data = self.get_serializer(request.data).data

        user = get_object_or_404(User, email=data['email'])
        user.send_password_confirm_email()

        return Response(
            data={'detail': _('Successfully Sent Reset Password Email')},
            status=200
        )


class ResetPasswordConfirmAPIView(GenericAPIView):
    serializer_class = ResetPasswordConfirmSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        rs_token = get_object_or_404(ResetPasswordToken, uid=data['uid'],
                                     token=data['token'])
        if (
                timezone.now() - rs_token.expiration_date).total_seconds() > 24 * 60 * 60:
            return Response({'error': 'Token Expired'}, status=400)

        user = get_object_or_404(User,
                                 id=urlsafe_base64_decode(data['uid']).decode(
                                     'utf-8'))
        rs_token.delete()
        user.password = make_password(data['new_password1'])
        user.save()
        return Response(data={'detail': _('Successfully Changed Password')},
                        status=200)



class ProfileAPIView(GenericAPIView):
    queryset = User.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser,)

    def get(self, request):
        user = request.user
        serializer = self.get_serializer(instance=user.profile)
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )

    def put(self, request):
        user = request.user
        serializer = self.get_serializer(instance=user.profile,
                                         data=request.data,
                                         partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            data=serializer.data,
            status=status.HTTP_201_CREATED
        )

    def delete(self, request):
        # to_be_deleted = self.request.query_params.get('file')
        # if not to_be_deleted or to_be_deleted not in ('image', 'resume'):
        #     return Response(status=status.HTTP_400_BAD_REQUEST)
        # if to_be_deleted == 'image':
        #     self.request.user.profile.image = None
        # else:
        #     self.request.user.profile.resume = None
        #
        # self.request.user.profile.save()
        #
        # return Response(status=status.HTTP_200_OK)
        pass
