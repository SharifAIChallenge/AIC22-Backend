from datetime import timedelta
from django.utils import timezone

from rest_framework import serializers

from AIC22_Backend.settings import SUBMISSION_COOLDOWN_IN_MINUTES, AIC_MINIO_DOMAIN
from challenge.models.submission import Submission
from constants import FILE_SIZE_LIMIT


class SubmissionSerializer(serializers.ModelSerializer):
    download_link = serializers.SerializerMethodField('_download_link')

    @staticmethod
    def _download_link(obj: Submission):
        url = obj.file.url
        if url:
            code_id = url[-40:-4]
            final_url = AIC_MINIO_DOMAIN + '/code/' + code_id
            return final_url
        return "null"

    class Meta:
        model = Submission
        fields = ['id', 'language', 'file', 'is_final', 'submit_time',
                  'download_link', 'status', 'infra_compile_message',
                  'is_mini_game', 'is_mini_game_final']
        # read_only_fields = (
        #     'id', 'is_final', 'submit_time',
        #     'user', 'download_link', 'status', 'infra_compile_message',
        #     'is_mini_game_final'
        # )

    def validate(self, attrs):
        user = self.context['request'].user

        attrs['user'] = user
        attrs['team'] = user.team
        if attrs['file'].size > FILE_SIZE_LIMIT:
            raise serializers.ValidationError('File size limit exceeded')
        submissions = user.team.submissions.all()
        if submissions.exists() and \
                timezone.now() - submissions.order_by('-submit_time')[0].submit_time \
                < timedelta(minutes=SUBMISSION_COOLDOWN_IN_MINUTES):
            raise serializers.ValidationError(
                f"You have to wait at least "
                f"{SUBMISSION_COOLDOWN_IN_MINUTES} "
                f"minute between each submission!"
            )

        return attrs

    def save(self, **kwargs):
        instance = super().save(**kwargs)
        instance.handle()
        return instance
