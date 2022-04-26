from django.shortcuts import render

# Create your views here.
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.translation import gettext_lazy as _
from account.models import Profile
from account.serializers import UserSerializer


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
