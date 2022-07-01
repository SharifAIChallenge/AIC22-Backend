from rest_framework import serializers

from .models import Staff, Tweet, Prize, PastAIC, FrequentlyAskedQuestions, News, NewsTag, StaffGroup, \
    StaffTeam, TimelineEvent, Statistic, UTMTracker
from utils import ImageURL


class StaffGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffGroup
        fields = '__all__'


class StaffTeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffTeam
        fields = '__all__'


class StaffSerializer(serializers.ModelSerializer, ImageURL):
    image_url = serializers.SerializerMethodField('_image_url')

    class Meta:
        model = Staff
        exclude = ('id',)


class TweetSerializer(serializers.ModelSerializer, ImageURL):
    image_url = serializers.SerializerMethodField('_image_url')

    class Meta:
        model = Tweet
        exclude = ('id',)


class PrizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prize
        exclude = ('id',)


class PastAICSerializer(serializers.ModelSerializer, ImageURL):
    image_url = serializers.SerializerMethodField('_image_url')

    class Meta:
        model = PastAIC
        exclude = ('id',)


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FrequentlyAskedQuestions
        exclude = ('id',)


class NewsSerializer(serializers.ModelSerializer):
    tags = serializers.SlugRelatedField(
        slug_field='title', many=True, queryset=NewsTag.objects.all()
    )

    class Meta:
        model = News
        fields = '__all__'


class NewsTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsTag
        exclude = ('id',)


class TimelineEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimelineEvent
        exclude = ('id',)


class StatisticSerializer(serializers.ModelSerializer):
    class Meta:
        model = Statistic
        exclude = ('id',)


class UTMTrackerSerializer(serializers.ModelSerializer):
    class Meta:
        model = UTMTracker
        exclude = ('count',)
