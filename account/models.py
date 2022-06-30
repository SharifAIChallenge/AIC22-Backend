import secrets

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.utils import timezone
from django.shortcuts import get_object_or_404

from AIC22_Backend import settings
from constants import SHORT_TEXT_MAX_LENGTH, MEDIUM_TEXT_MAX_LENGTH, LONG_TEXT_MAX_LENGTH
# from team.models import Team
from .utils import send_email

from multiselectfield import MultiSelectField


class DegreeTypes:
    ST = 'دانش‌ آموز'
    BA = 'کارشناسی'
    MA = 'کارشناسی ارشد'
    DO = 'دکترا'

    TYPES = (
        ('ST', ST),
        ('BA', BA),
        ('MA', MA),
        ('DO', DO)
    )


class ProgrammingLanguages:
    JAVA = 'Java'
    PYTHON3 = 'Python 3'
    CPP = 'C++'

    TYPES = (
        ('Java', JAVA),
        ('Python 3', PYTHON3),
        ('C++', CPP)
    )


class User(AbstractUser):
    team = models.ForeignKey(to='team.Team',
                             on_delete=models.SET_NULL,
                             related_name='members', null=True, blank=True)

    def send_activation_email(self):
        activate_user_token = ActivateUserToken(
            token=secrets.token_urlsafe(32),
            eid=urlsafe_base64_encode(force_bytes(self.email)),
        )
        activate_user_token.save()

        context = {
            'domain': settings.AIC_DOMAIN,
            'eid': activate_user_token.eid,
            'token': activate_user_token.token,
            'first_name': self.profile.firstname_en
        }

        send_email(
            subject='فعالسازی حساب AIC22',
            context=context,
            template_name='accounts/email/registerifinal.html',
            receipts=[self.email]
        )

    def reject_all_pending_invites(self):
        invitations = self.invitations.filter(status="pending")
        invitations.update(status="rejected")

    def send_password_confirm_email(self):
        uid = urlsafe_base64_encode(force_bytes(self.id))
        ResetPasswordToken.objects.filter(uid=uid).delete()
        reset_password_token = ResetPasswordToken(
            uid=uid,
            token=secrets.token_urlsafe(32),
            expiration_date=timezone.now() + timezone.timedelta(hours=24),
        )
        reset_password_token.save()
        context = {
            'domain': settings.AIC_DOMAIN,
            'username': self.username,
            'uid': reset_password_token.uid,
            'token': reset_password_token.token,
        }
        send_email(
            subject='تغییر رمز عبور AIC22',
            context=context,
            template_name='accounts/email/user_reset_password.html',
            receipts=[self.email]
        )

    @classmethod
    def activate(cls, eid, token):
        activate_user_token = get_object_or_404(ActivateUserToken,
                                                eid=eid, token=token)

        email = urlsafe_base64_decode(eid).decode('utf-8')
        user = cls.objects.get(email=email)
        user.is_active = True
        activate_user_token.delete()
        user.save()


class Profile(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, related_name='profile')

    # Personal Information
    firstname_en = models.CharField(max_length=SHORT_TEXT_MAX_LENGTH, null=True, blank=True)
    firstname_fa = models.CharField(max_length=SHORT_TEXT_MAX_LENGTH, null=True, blank=True)
    lastname_en = models.CharField(max_length=SHORT_TEXT_MAX_LENGTH, null=True, blank=True)
    lastname_fa = models.CharField(max_length=SHORT_TEXT_MAX_LENGTH, null=True, blank=True)
    # birth_year = models.IntegerField(null=True, blank=True)
    phone_number = models.CharField(max_length=SHORT_TEXT_MAX_LENGTH, null=True, blank=True)
    province = models.CharField(max_length=SHORT_TEXT_MAX_LENGTH, blank=True, null=True)
    city = models.CharField(max_length=SHORT_TEXT_MAX_LENGTH, blank=True, null=True)
    address = models.CharField(max_length=MEDIUM_TEXT_MAX_LENGTH, blank=True, null=True)

    # Academic Information
    university = models.CharField(max_length=SHORT_TEXT_MAX_LENGTH, blank=True, null=True)
    major = models.CharField(max_length=SHORT_TEXT_MAX_LENGTH, blank=True, null=True)
    university_term = models.PositiveSmallIntegerField(null=True, blank=True)
    university_degree = models.CharField(choices=DegreeTypes.TYPES,
                                         max_length=SHORT_TEXT_MAX_LENGTH,
                                         null=True, blank=True)

    # Job and Social Information
    linkedin = models.CharField(max_length=MEDIUM_TEXT_MAX_LENGTH, blank=True, null=True)
    github = models.CharField(max_length=MEDIUM_TEXT_MAX_LENGTH, null=True, blank=True)
    resume = models.FileField(upload_to="resumes", null=True, blank=True)
    # programming_languages = MultiSelectField(choices=ProgrammingLanguages.TYPES, max_choices=3, default=None)

    # Others
    image = models.ImageField(upload_to='profile_images', null=True, blank=True)
    hide_profile_info = models.BooleanField(default=False)
    can_sponsors_see = models.BooleanField(default=True)

    @property
    def is_complete(self):
        return all(
            (
                self.university, self.university_degree, self.major,
                self.phone_number, self.firstname_fa,
                self.lastname_fa
            )
        )

    @staticmethod
    def sensitive_fields():
        return ('hide_profile_info', 'can_sponsors_see', 'phone_number',
                'province', 'is_complete', 'resume',)


class ProgrammingLanguage(models.Model):
    programming_language_title = models.CharField(choices=ProgrammingLanguages.TYPES, max_length=SHORT_TEXT_MAX_LENGTH)
    profile = models.ForeignKey(to=Profile,
                                related_name='programming_languages',
                                on_delete=models.CASCADE)

    def __str__(self):
        return self.programming_language_title


class Skill(models.Model):
    skill = models.CharField(max_length=MEDIUM_TEXT_MAX_LENGTH)
    profile = models.ForeignKey(to=Profile,
                                related_name='skills',
                                on_delete=models.CASCADE)

    def __str__(self):
        return str(self.skill)


class JobExperience(models.Model):
    company = models.CharField(max_length=SHORT_TEXT_MAX_LENGTH, blank=True,
                               null=True)
    position = models.CharField(max_length=SHORT_TEXT_MAX_LENGTH, blank=True, null=True)
    working_years = models.PositiveSmallIntegerField(blank=True, null=True)
    description = models.CharField(max_length=LONG_TEXT_MAX_LENGTH, blank=True, null=True)
    profile = models.ForeignKey(
        to=Profile,
        related_name='jobs',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return str(self.position)


class ActivateUserToken(models.Model):
    token = models.CharField(max_length=100)
    eid = models.CharField(max_length=100, null=True)


class ResetPasswordToken(models.Model):
    uid = models.CharField(max_length=100)
    token = models.CharField(max_length=100)
    expiration_date = models.DateTimeField()


class GoogleLogin(models.Model):
    access_token = models.CharField(max_length=1024)
    expires_at = models.PositiveIntegerField()
    expires_in = models.PositiveIntegerField()
    id_token = models.TextField()
    scope = models.TextField()
    is_signup = models.BooleanField(default=False)
    email = models.EmailField(blank=True, null=True)

