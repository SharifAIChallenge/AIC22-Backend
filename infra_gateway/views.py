from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status

from infra_gateway.permissions import IsInfra
from infra_gateway.serializers import InfraEventPushSerializer


class InfraEventPushAPIView(GenericAPIView):
    serializer_class = InfraEventPushSerializer
    permission_classes = (IsInfra,)

    def post(self, request):
        serializer = self.get_serializer(
            data=request.data
        )
        print(request.data)
        print('--------------------------------')
        print(request.headers)

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(
            data={
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )
