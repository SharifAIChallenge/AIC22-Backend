from django.contrib.auth.hashers import make_password
from django.db import transaction
from django.db.models import Value
from django.db.models.functions import Concat
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.http import urlsafe_base64_decode
from rest_framework import status, serializers, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _
from account.models import Profile, User, ResetPasswordToken
from account.paginations import CustomPagination
from account.permissions import ProfileComplete
from account.serializers import UserSerializer, EmailSerializer, ProfileSerializer, GoogleLoginSerializer, \
    ChangePasswordSerializer, ResetPasswordConfirmSerializer, UserViewSerializer


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
                # for without activation signup system
                # user.send_successful_register_email()
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
        return Response(data={'detail': _('Account Activated')}, status=status.HTTP_200_OK)


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
            user = get_object_or_404(User, email=serializer.validated_data['email'])
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

        rs_token = get_object_or_404(ResetPasswordToken, uid=data['uid'], token=data['token'])
        if (timezone.now() - rs_token.expiration_date).total_seconds() > 24 * 60 * 60:
            return Response({'error': 'Token Expired'}, status=400)

        user = get_object_or_404(User, id=urlsafe_base64_decode(data['uid']).decode('utf-8'))
        rs_token.delete()
        user.password = make_password(data['new_password1'])
        user.save()
        return Response(data={'detail': _('Successfully Changed Password')}, status=200)


class ProfileAPIView(GenericAPIView):
    queryset = User.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = self.get_serializer(instance=user.profile)  # todo warning
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )

    def put(self, request):
        user = request.user
        serializer = self.get_serializer(instance=user.profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            data=serializer.data,
            status=status.HTTP_201_CREATED
        )

    def delete(self, request):
        pass


class UserWithoutTeamAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated, ProfileComplete]
    serializer_class = UserViewSerializer
    pagination_class = CustomPagination

    def get(self, request):

        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        data = self.get_serializer(
            instance=page,
            many=True
        ).data

        return self.get_paginated_response(
            data={'data': data},
        )

    def get_queryset(self):
        name = self.request.query_params.get('name')
        email = self.request.query_params.get('email')
        university = self.request.query_params.get('university')
        programming_language = self.request.query_params.get('programming_language')
        major = self.request.query_params.get('major')

        queryset = User.objects.all().filter(team=None).exclude(profile=None)

        if name:
            queryset = queryset.annotate(
                name=Concat('profile__firstname_fa', Value(' '),
                            'profile__lastname_fa')
            ).filter(name__icontains=name)

        if email:
            queryset = queryset.filter(
                email__icontains=email
            )

        if university:
            queryset = queryset.filter(
                profile__university__icontains=university
            )

        if programming_language:
            queryset = queryset.filter(
                profile__programming_language=programming_language
            )

        if major:
            queryset = queryset.filter(
                profile__major__icontains=major
            )
        complete_profiles = [user.id for user in
                             filter(lambda user: user.profile.is_complete,
                                    queryset
                                    )
                             ]
        queryset = queryset.filter(id__in=complete_profiles)
        return queryset
