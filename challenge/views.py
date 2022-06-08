from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_tracking.mixins import LoggingErrorsMixin

from team.permissions import HasTeam, IsFinalist
from .models.submission import Submission
from .serializers import SubmissionSerializer


class SubmissionsListAPIView(GenericAPIView):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    permission_classes = (IsAuthenticated, HasTeam)

    def get(self, request):
        data = self.get_serializer(
            self.get_queryset().filter(team=request.user.team),
            many=True).data
        return Response(data={'submissions': data}, status=status.HTTP_200_OK)


class SubmissionAPIView(LoggingErrorsMixin, GenericAPIView):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    permission_classes = (IsAuthenticated, HasTeam, IsFinalist)

    def get(self, request):
        data = self.get_serializer(
            self.get_queryset().filter(team=request.user.team),
            many=True).data
        return Response(data=data, status=status.HTTP_200_OK)

    def post(self, request):
        submission = self.get_serializer(
            data=request.data,
            context={'request': request}
        )
        if submission.is_valid(raise_exception=True):
            submission = submission.save()
            return Response(
                data={'submission_id': submission.id},
                status=status.HTTP_200_OK
            )
        return Response(
            data={'errors': 'Something Went Wrong'},
            status=status.HTTP_406_NOT_ACCEPTABLE
        )

    # def put(self, request, submission_id):
    #     submission = get_object_or_404(Submission, id=submission_id)
    #     try:
    #         submission.set_final()
    #         return Response(
    #             data={'details': 'Final submission changed successfully'},
    #             status=status.HTTP_200_OK
    #         )
    #     except ValueError as e:
    #         return Response(data={'errors': [str(e)]},
    #                         status=status.HTTP_406_NOT_ACCEPTABLE)
