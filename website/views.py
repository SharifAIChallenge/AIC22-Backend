from rest_framework import mixins, status, filters
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import Staff, Tweet, Prize, PastAIC, FrequentlyAskedQuestions, News, NewsTag, StaffGroup, StaffTeam, \
    TimelineEvent, Statistic, UTMTracker
from .serializers import StaffSerializer, TweetSerializer, PrizeSerializer, PastAICSerializer, FAQSerializer, \
    NewsSerializer, NewsTagSerializer, StaffGroupSerializer, StaffTeamSerializer, \
    TimelineEventSerializer, StatisticSerializer, UTMTrackerSerializer
from permissions import AdminWritePermission


class StaffsListViewSet(
    GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin
):
    serializer_class = StaffSerializer
    permission_classes = (AdminWritePermission, )
    filter_backends = [DjangoFilterBackend]

    filterset_fields = ['team__group', 'team', 'role']

    def get_queryset(self):
        return Staff.objects.all().order_by('team', '-role')

    @action(
        detail=False,
        serializer_class=StaffGroupSerializer
    )
    def groups(self, request):
        queryset = StaffGroup.objects.all()
        serializer = self.get_serializer(queryset, many=True)
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
        url_path=r'random/(?P<number>\d+)',
        filter_backends=[DjangoFilterBackend],
        filterset_fields=['team__group', 'team', 'role'],
    )
    def random(self, request, number):
        queryset = self.filter_queryset(queryset=self.get_queryset())
        queryset = queryset.order_by('?')[:int(number)]
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
    serializer_class = PastAICSerializer
    permission_classes = (AdminWritePermission,)

    def get_queryset(self):
        return PastAIC.objects.all().order_by('event_year')


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
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
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


class StatisticViewSet(GenericViewSet, mixins.ListModelMixin):
    queryset = Statistic.objects.all()
    serializer_class = StatisticSerializer
    permission_classes = (AdminWritePermission,)


class UTMTrackerViewSet(GenericViewSet, mixins.CreateModelMixin, mixins.RetrieveModelMixin):
    queryset = UTMTracker.objects.all()
    serializer_class = UTMTrackerSerializer
    permission_classes = (AdminWritePermission,)

    def retrieve(self, request, *args, **kwargs):
        self.get_object().increase()
        return Response({}, status=status.HTTP_200_OK)
