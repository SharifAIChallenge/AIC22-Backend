from django.shortcuts import get_object_or_404
from rest_framework import status, serializers
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import GenericAPIView
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _
from account.models import Profile, User
from account.serializers import UserSerializer, EmailSerializer, ProfileSerializer


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


class ProfileAPIView(GenericAPIView):
    queryset = User.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def get(self, request):
        user = request.user
        serializer = self.get_serializer(instance=user.profile)
        return Response(
            data={'data': serializer.data},
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
            data={'data': serializer.data},
            status=status.HTTP_200_OK
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
