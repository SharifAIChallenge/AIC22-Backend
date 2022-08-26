from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status

from infra_gateway.permissions import IsInfra
from infra_gateway.serializers import InfraEventPushSerializer

from challenge.models.match import Match

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

        print("////// Check validation //////")
        serializer.is_valid(raise_exception=True)

        print("/////////////// Save ///////////////")
        serializer.save()

        print("/////////// Send response ///////")
        return Response(
            data={
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )

class InfraCheckGameAPIView(GenericAPIView):
    def get(self, request):
        token = request.query_params.get("token")
        matches = Match.objects.filter(infra_token=token)
        if not matches:
            return Response(status=404) 
        return Response(
            status=status.HTTP_200_OK
        )