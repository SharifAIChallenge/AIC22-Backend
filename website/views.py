from rest_framework import mixins, status, filters
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from django.contrib.sites.shortcuts import get_current_site
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import Staff, Tweet, Prize, PastAIC, FrequentlyAskedQuestions, News, NewsTag, StaffGroup, StaffTeam, \
                    TimelineEvent
from .serializers import StaffSerializer, TweetSerializer, PrizeSerializer, PastAICSerializer, FAQSerializer, \
                         NewsSerializer, NewsTagSerializer, StaffGroupSerializer, StaffTeamSerializer, \
                         TimelineEventSerializer
from permissions import AdminWritePermission


class StaffsListViewSet(
    GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin
):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
    permission_classes = (AdminWritePermission, )
    filter_backends = [DjangoFilterBackend]

    filterset_fields = ['team__group', 'team', 'role']

    @action(
        detail=False,
        serializer_class=StaffGroupSerializer
    )
    def groups(self, request):
        queryset = StaffGroup.objects.all()
        serializer = self.get_serializer(queryset, many=True)
        # data = {'shit': get_current_site(request).domain}
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=False,
        serializer_class=StaffTeamSerializer,
        url_path=r'teams/(?P<group_pk>\w+)'
    )
    def teams(self, request, group_pk):
        queryset = StaffTeam.objects.filter(group=group_pk)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=False,
        url_path=r'random/(?P<number>\d+)'
    )
    def random(self, request, number):
        queryset = Staff.objects.order_by('?')[:int(number)]
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TweetsListViewSet(
    GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin
):
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer
    permission_classes = (AdminWritePermission,)


class PrizesListViewSet(
    GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin
):
    queryset = Prize.objects.all()
    serializer_class = PrizeSerializer
    permission_classes = (AdminWritePermission,)


class PastAICsListViewSet(
    GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin
):
    queryset = PastAIC.objects.all()
    serializer_class = PastAICSerializer
    permission_classes = (AdminWritePermission,)


class FAQListViewSet(
    GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin
):
    queryset = FrequentlyAskedQuestions.objects.all()
    serializer_class = FAQSerializer
    permission_classes = (AdminWritePermission, )
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['show_on_landing_page']


class NewsListViewSet(
    GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin
):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = (AdminWritePermission,)
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = ['importance']
    ordering_fields = ['post_time']


class NewsTagListViewSet(
    GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin
):
    queryset = NewsTag.objects.all()
    serializer_class = NewsTagSerializer
    permission_classes = (AdminWritePermission,)


class TimelineEventListViewSet(
    GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin
):
    queryset = TimelineEvent.objects.all()
    serializer_class = TimelineEventSerializer
    permission_classes = (AdminWritePermission,)
