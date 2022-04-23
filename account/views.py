from django.shortcuts import get_object_or_404

from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from rest_framework import status

from .serializers import ProfileSerializer
from .models import User


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
        to_be_deleted = self.request.query_params.get('file')
        if not to_be_deleted or to_be_deleted not in ('image', 'resume'):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if to_be_deleted == 'image':
            self.request.user.profile.image = None
        else:
            self.request.user.profile.resume = None

        self.request.user.profile.save()

        return Response(status=status.HTTP_200_OK)


class HideProfileInfoAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        request.user.profile.hide_profile_info =\
            not request.user.profile.hide_profile_info

        return Response(status=status.HTTP_200_OK)
