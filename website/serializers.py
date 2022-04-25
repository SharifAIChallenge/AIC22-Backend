from django.conf import settings

from rest_framework import serializers

from .models import Staff, Tweet, Prize, PastAIC


class StaffSerializer(serializers.ModelSerializer):

    class Meta:
        model = Staff
        exclude = ('id', )


class TweetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tweet
        exclude = ('id',)


class PrizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prize
        exclude = ('id',)


class PastAICSerializer(serializers.ModelSerializer):
    class Meta:
        model = PastAIC
        exclude = ('id',)
