import requests

from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator

from account.exceptions import ProgrammingLanguageNotFound
from account.models import GoogleLogin, ResetPasswordToken
from account.models import User, Profile, Skill, JobExperience, ProgrammingLanguage
from account.utils import password_generator
from constants import MEDIUM_TEXT_MAX_LENGTH
from team.models import Invitation, InvitationTypes
from utils import ImageURL
from website.models import UTMTracker


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password_1 = serializers.CharField(
        style={'input_type': 'password'}
    )
    password_2 = serializers.CharField(
        style={'input_type': 'password'}
    )
    utm_id = serializers.CharField(write_only=True, allow_null=True)

    class Meta:
        model = User
        fields = ['email', 'password_1', 'password_2', 'utm_id']

    def validate(self, attrs):
        if attrs.get('password_1') != attrs.get('password_2'):
            raise ValidationError(_("Passwords not match"))

        return attrs

    def create(self, validated_data):
        validated_data.pop('password_2')
        validated_data['password'] = validated_data.pop('password_1')

        user = User.objects.create_user(
            username=validated_data.get('email'),
            email=validated_data.get('email'),
            password=validated_data.get('password'),
            is_active=False
        )
        Profile.objects.create(
            user=user,
        )
        utm_tracker = UTMTracker.objects.filter(code=validated_data['utm_id'])
        if utm_tracker.count() == 1:
            utm_tracker = utm_tracker.first()
            utm_tracker.increase_sign_up_count()
        return user


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ResetPasswordConfirmSerializer(serializers.ModelSerializer):
    new_password1 = serializers.CharField(max_length=100)
    new_password2 = serializers.CharField(max_length=100)

    class Meta:
        model = ResetPasswordToken
        fields = ['new_password1', 'new_password2', 'uid', 'token']

    def validate(self, data):
        if data['new_password1'] != data['new_password2']:
            raise serializers.ValidationError('passwords don\'t match!')
        return data


class ProgrammingLanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgrammingLanguage
        fields = ('programming_language_title',)

    def create(self, validated_data):
        validated_data['profile'] = self.context['request'].user.profile

        return ProgrammingLanguage.objects.create(**validated_data)


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
        fields = ('company', 'position', 'working_years', 'description')

    def create(self, validated_data):
        validated_data['profile'] = self.context['request'].user.profile

        return JobExperience.objects.create(**validated_data)


class StringListField(serializers.ListField):
    child = serializers.CharField(max_length=MEDIUM_TEXT_MAX_LENGTH, allow_null=True,
                                  allow_blank=True)


class ShortProfileSerializer(serializers.ModelSerializer, ImageURL):
    programming_languages = ProgrammingLanguageSerializer(many=True, read_only=True)
    image_url = serializers.SerializerMethodField('_image_url')
    has_team = serializers.SerializerMethodField('_has_team')

    @staticmethod
    def _has_team(obj: Profile):
        return obj.user.team is not None

    class Meta:
        model = Profile
        fields = [
            'firstname_en',
            'firstname_fa',
            'lastname_en',
            'lastname_fa',
            'programming_languages',
            'image_url',
            'has_team',
        ]


class ProfileSerializer(serializers.ModelSerializer, ImageURL):
    skills = SkillSerializer(many=True, read_only=True)
    jobs = JobExperienceSerializer(many=True, read_only=True)
    programming_languages = ProgrammingLanguageSerializer(many=True, read_only=True)
    skills_list = StringListField(write_only=True, allow_null=True,
                                  allow_empty=True)
    jobs_list = StringListField(write_only=True, allow_null=True,
                                allow_empty=True)
    programming_languages_list = serializers.CharField(write_only=True, allow_null=True)
    email = serializers.SerializerMethodField('_email')
    # programming_languages = fields.MultipleChoiceField(choices=ProgrammingLanguages.TYPES)
    image_url = serializers.SerializerMethodField('_image_url')
    resume_url = serializers.SerializerMethodField('_resume_url')
    is_complete = serializers.SerializerMethodField('_is_complete')
    has_team = serializers.SerializerMethodField('_has_team')

    @staticmethod
    def _has_team(obj: Profile):
        return obj.user.team is not None

    @staticmethod
    def _is_complete(obj: Profile):
        return obj.is_complete

    @staticmethod
    def _email(obj: Profile):
        return obj.user.email

    class Meta:
        model = Profile
        exclude = ['user', 'id', ]

    def update(self, instance, validated_data):
        ProgrammingLanguage.objects.filter(profile=instance).delete()
        languages = validated_data.get('programming_languages_list', "").split(',')
        for language in languages:
            if language.lower() not in ['java', 'c++', 'python 3']:
                raise ProgrammingLanguageNotFound()
            ProgrammingLanguage.objects.create(
                profile=instance,
                programming_language_title=language,
            )
        Skill.objects.filter(profile=instance).delete()
        for skill in validated_data.get('skills_list', []):
            Skill.objects.create(
                profile=instance,
                skill=skill
            )
        JobExperience.objects.filter(profile=instance).delete()
        job_data = validated_data.get('jobs_list', [])
        if len(job_data) % 4 != 0:
            raise Exception
        for i in range(0, len(job_data), 4):
            JobExperience.objects.create(
                profile=instance,
                company=job_data[i],
                position=job_data[i+1],
                working_years=int(job_data[i+2]),
                description=job_data[i+3]
            )

        return super().update(instance, validated_data)


class GoogleLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoogleLogin
        exclude = ('id',)

    def create(self, validated_data):

        response = requests.get(
            f'https://www.googleapis.com/oauth2/v3/tokeninfo?access_token='
            f'{validated_data["access_token"]}'
        )

        if response.status_code != 200:
            raise ValidationError("Error occurred with google login")

        data = response.json()
        validated_data['email'] = data['email']

        user = User.objects.filter(email=data['email']).last()
        if user and not user.is_active:
            user.is_active = True
            user.save()
        if not user:
            validated_data['is_signup'] = True
            user = User.objects.create(
                username=data['email'],
                email=data['email'],
                password=password_generator(),
                is_active=True
            )
            Profile.objects.create(
                user=user
            )

        super().create(validated_data)
        token, created = Token.objects.get_or_create(user=user)
        return token


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(style={'input_type': 'password'})
    new_password1 = serializers.CharField(style={'input_type': 'password'})
    new_password2 = serializers.CharField(style={'input_type': 'password'})

    def validate(self, data):
        if data['new_password1'] != data['new_password2']:
            raise serializers.ValidationError(_('passwords don\'t match!'))
        if not self.context['request'].user.check_password(
                data['old_password']):
            raise serializers.ValidationError(_('invalid old password'))
        return data

    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(
            raw_password=self.validated_data['new_password1']
        )
        user.save()

        return user


class UserViewSerializer(serializers.ModelSerializer):
    profile = ShortProfileSerializer()
    team_status = serializers.SerializerMethodField('_get_status')

    def _get_status(self, obj):
        user_team = self.context['request'].user.team
        if not user_team:
            return None
        last_invitation = Invitation.objects.filter(
            user=obj,
            type=InvitationTypes.TEAM_TO_USER,
            team=user_team
        ).last()
        if not last_invitation:
            return None
        return last_invitation.status

    class Meta:
        model = User
        fields = ['profile', 'email', 'id', 'team_status']
