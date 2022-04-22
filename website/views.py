from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from .models import Staff, FrequentlyAskedQuestions
from .serializers import StaffSerializer, FAQSerializer
from permissions import AdminWritePermission


class StaffsListViewSet(
    GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin
):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
    permission_classes = (AdminWritePermission, )


class FAQListViewSet(
    GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin
):
    queryset = FrequentlyAskedQuestions.objects.all()
    serializer_class = FAQSerializer
    permission_classes = (AdminWritePermission, )
