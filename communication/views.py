from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated, \
    IsAdminUser
from rest_framework.response import Response

from account.permissions import ProfileComplete
from .serializers import LimitedTicketSerializer, ReplySerializer, TagSerializer, TicketSerializer
from .models import Reply, Tag, Ticket
from .services.telegram import TelegramInterface


class TicketAPIView(GenericAPIView):
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated, IsAdminUser | ProfileComplete]

    def get(self, request, ticket_id):
        ticket = get_object_or_404(Ticket, id=ticket_id)
        data = self.get_serializer(instance=ticket).data

        return Response(
            data={'data': data},
            status=status.HTTP_200_OK
        )

    def put(self, request, ticket_id):
        ticket = get_object_or_404(Ticket, id=ticket_id)
        serializer = self.get_serializer(instance=ticket, data=request.data,
                                         partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            data={"detail": "Your change has been submitted"},
            status=status.HTTP_200_OK
        )


class UserTicketsListAPIView(GenericAPIView):
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated, ProfileComplete | IsAdminUser]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        ticket = serializer.save()

        telegram = TelegramInterface(
            ticket=ticket,
            reply=None
        )
        telegram.send()

        return Response(
            data={"detail": "Your ticket has been submitted"},
            status=status.HTTP_201_CREATED
        )

    def get(self, request):
        tickets = Ticket.objects.filter(
            author=request.user
        )
        data = LimitedTicketSerializer(instance=tickets, many=True).data

        return Response(
            data={'data': data},
            status=status.HTTP_200_OK
        )


class PublicTicketsListAPIView(GenericAPIView):
    serializer_class = TicketSerializer

    def get(self, request):
        tickets = Ticket.objects.filter(is_public=True)
        data = LimitedTicketSerializer(instance=tickets, many=True).data
        return Response(
            data={'data': data},
            status=status.HTTP_200_OK
        )


class AdminTicketsListAPIView(GenericAPIView):
    serializer_class = LimitedTicketSerializer
    queryset = Ticket.objects.all()
    permission_classes = (IsAdminUser,)

    def get(self, request):
        tickets = self.get_queryset().order_by('-status')
        data = self.get_serializer(instance=tickets, many=True).data
        return Response(
            data={'data': data},
            status=status.HTTP_200_OK
        )


class ReplyListAPIView(GenericAPIView):
    serializer_class = ReplySerializer
    queryset = Reply.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser | ProfileComplete]

    def get(self, request, ticket_id):
        replies = self.get_queryset().filter(ticket__id=ticket_id)
        # data = ReplySerializer(replies, many=True, context={'request': request}).data
        data = self.get_serializer(replies, many=True).data
        return Response(data)

    def post(self, request, ticket_id):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        reply = serializer.save()

        telegram = TelegramInterface(
            ticket=reply.ticket,
            reply=reply
        )

        telegram.send()

        return Response({"detail": "Your Reply has been submitted"})

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['ticket_id'] = self.kwargs.get('ticket_id')
        return context


class ReplyAPIView(GenericAPIView):
    serializer_class = ReplySerializer
    permission_classes = [IsAuthenticated, IsAdminUser | ProfileComplete]

    def get(self, request, ticket_id, reply_id):
        reply = get_object_or_404(Reply, id=reply_id)
        data = self.get_serializer(instance=reply).data

        return Response(
            data={'data': data},
            status=status.HTTP_200_OK
        )

    def put(self, request, ticket_id, reply_id):
        reply = get_object_or_404(Reply, id=reply_id)
        serializer = self.get_serializer(instance=reply, data=request.data,
                                         partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            data={"detail": "Your change has been submitted"},
            status=status.HTTP_200_OK
        )


class TagAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated, ProfileComplete | IsAdminUser)
    serializer_class = TagSerializer
    queryset = Tag.objects.all()

    def get(self, request):
        data = self.get_serializer(
            instance=self.get_queryset(),
            many=True
        ).data

        return Response(
            data={'data': data},
            status=status.HTTP_200_OK
        )

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            data={"detail": "Tag is created"},
            status=status.HTTP_200_OK
        )
