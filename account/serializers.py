from django.conf import settings

from rest_framework import serializers

from .models import Skill, Profile, JobExperience
from constants import IMAGE_MAX_SIZE


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ('skill',)

    def create(self, validated_data):
        validated_data['profile'] = self.context['request'].user.profile

        return Skill.objects.create(**validated_data)


class JobExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobExperience
        fields = ('company', 'position', 'working_years',  'description')

    def create(self, validated_data):
        validated_data['profile'] = self.context['request'].user.profile

        return JobExperience.objects.create(**validated_data)


class StringListField(serializers.ListField):
    child = serializers.CharField(max_length=256, allow_null=True,
                                  allow_blank=True)


class ProfileSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True, read_only=True)
    jobs = JobExperienceSerializer(many=True, read_only=True)
    skills_list = StringListField(write_only=True, allow_null=True,
                                  allow_empty=True)
    jobs_list = StringListField(write_only=True, allow_null=True,
                                allow_empty=True)
    is_complete = serializers.SerializerMethodField('_is_complete')
    email = serializers.SerializerMethodField('_email')
    resume_link = serializers.SerializerMethodField('_get_resume_link')
    image_link = serializers.SerializerMethodField('_get_image_link')
    has_team = serializers.SerializerMethodField('_has_team')
    is_finalist = serializers.SerializerMethodField('_is_finalist')

    @staticmethod
    def _has_team(obj: Profile):
        return obj.user.team is not None

    @staticmethod
    def _is_finalist(obj: Profile):
        if obj.user.team:
            return obj.user.team.is_finalist
        return False

    @staticmethod
    def _is_complete(obj: Profile):
        return obj.is_complete

    @staticmethod
    def _email(obj: Profile):
        return obj.user.email

    @staticmethod
    def _get_resume_link(obj: Profile):
        if not obj.resume:
            return ''
        url = obj.resume.url
        if settings.DOMAIN not in url:
            return settings.DOMAIN + url
        return url

    @staticmethod
    def _get_image_link(obj: Profile):
        if not obj.image:
            return ''
        url = obj.image.url
        if settings.DOMAIN not in url:
            return settings.DOMAIN + url
        return url

    class Meta:
        model = Profile
        exclude = ['user', 'id', 'phone_number', 'national_code']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if self.context.get('limited', False):
            for field in Profile.sensitive_fields():
                data.pop(field)
        return data

    def validate(self, attrs):
        image = attrs.get('image')

        if image and image.size > IMAGE_MAX_SIZE:
            raise serializers.ValidationError('Maximum file size reached')

        return attrs

    def update(self, instance: Profile, validated_data):
        instance: Profile = super().update(instance, validated_data)

        jobs = validated_data.get('jobs_list')
        skills = validated_data.get('skills_list')

        if not jobs:
            jobs = list()
        if not skills:
            skills = list()

        if jobs:
            instance.jobs.all().delete()
        if skills:
            instance.skills.all().delete()

        for job in jobs:
            if job:
                JobExperience.objects.create(
                    position=job,
                    profile=instance
                )

        for skill in skills:
            if skill:
                Skill.objects.create(
                    skill=skill,
                    profile=instance
                )
        return instance
