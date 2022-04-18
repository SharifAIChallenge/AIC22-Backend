from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from .models import Staff
from .serializers import StaffSerializer
from permissions import AdminWritePermission


class StaffsListViewSet(
    GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin
):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
    permission_classes = (AdminWritePermission, )
