from rest_framework import serializers

from account.serializers import ProfileSerializer
from .models import Tag, Reply, Ticket
from account.models import User



class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'title')


class TicketUserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ('email', 'profile')


class ReplySerializer(serializers.ModelSerializer):
    user = TicketUserSerializer(read_only=True)
    is_owner = serializers.SerializerMethodField('_is_owner')

    def _is_owner(self, obj: Reply):
        return obj.user.id == self.context['request'].user.id

    class Meta:
        model = Reply
        fields = ('user', 'text', 'created', 'status', 'id', 'is_owner')
        read_only_fields = ('user', 'status', 'created', 'id', 'is_owner')

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        validated_data['ticket_id'] = self.context['ticket_id']

        return Reply.objects.create(**validated_data)


class LimitedTicketSerializer(serializers.ModelSerializer):
    num_replies = serializers.SerializerMethodField()

    @staticmethod
    def get_num_replies(obj):
        return obj.replies.count()

    class Meta:
        model = Ticket
        fields = ('num_replies', 'tag', 'id',
                  'title', 'status', 'is_public')
        read_only_fields = ('author',)


class TicketSerializer(serializers.ModelSerializer):
    author = TicketUserSerializer(read_only=True)
    num_replies = serializers.SerializerMethodField()

    @staticmethod
    def get_num_replies(obj):
        return obj.replies.count()

    class Meta:
        model = Ticket
        fields = ('author', 'num_replies', 'tag', 'id',
                  'title', 'text', 'status', 'is_public')
        read_only_fields = ('author',)

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        ticket = Ticket.objects.create(**validated_data)
        return ticket

    def to_representation(self, instance: Ticket):
        data = super().to_representation(instance)

        replies = instance.replies.all()
        data['replies'] = ReplySerializer(
            instance=replies,
            many=True,
            context={'request': self.context['request']}
        ).data
        
        return data
