

from django.utils.translation import gettext_lazy as _
from rest_framework import serializers, fields
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator

from account.models import User, Profile, Skill, JobExperience, ProgrammingLanguages


class UserSerializer(serializers.ModelSerializer):
    # profile = ProfileSerializer(read_only=True)

    phone_number = serializers.CharField(
        max_length=32,
        required=True,
    )
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password_1 = serializers.CharField(
        style={'input_type': 'password'}
    )
    password_2 = serializers.CharField(
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = ['email', 'phone_number', 'password_1', 'password_2',
                  'profile']
        read_only_fields = ['profile']

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
            phone_number=validated_data.get('phone_number')
        )

        return user


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()


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
    email = serializers.SerializerMethodField('_email')
    programming_languages = fields.MultipleChoiceField(choices=ProgrammingLanguages.TYPES)

    @staticmethod
    def _email(obj: Profile):
        return obj.user.email

    class Meta:
        model = Profile
        exclude = ['user', 'id', ]
