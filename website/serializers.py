from rest_framework import serializers

from .models import Staff, FrequentlyAskedQuestions


class StaffSerializer(serializers.ModelSerializer):

    class Meta:
        model = Staff
        exclude = ('id', )


class FAQSerializer(serializers.ModelSerializer):

    class Meta:
        model = FrequentlyAskedQuestions
        exclude = ('id', )
