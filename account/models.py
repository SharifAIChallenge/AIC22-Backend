from django.db import models
from django.contrib.auth.models import AbstractUser

from constants import SHORT_TEXT_MAX_LENGTH, MEDIUM_TEXT_MAX_LENGTH, LONG_TEXT_MAX_LENGTH


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


class User(AbstractUser):
    pass


class Profile(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.PROTECT, related_name='profile')

    # Personal Information
    firstname_en = models.CharField(max_length=SHORT_TEXT_MAX_LENGTH, null=True, blank=True)
    firstname_fa = models.CharField(max_length=SHORT_TEXT_MAX_LENGTH, null=True, blank=True)
    lastname_en = models.CharField(max_length=SHORT_TEXT_MAX_LENGTH, null=True, blank=True)
    lastname_fa = models.CharField(max_length=SHORT_TEXT_MAX_LENGTH, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=SHORT_TEXT_MAX_LENGTH, null=True, blank=True)
    national_code = models.CharField(max_length=SHORT_TEXT_MAX_LENGTH, null=True, blank=True)
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

    # Others
    image = models.ImageField(upload_to='profile_images', null=True, blank=True)
    hide_profile_info = models.BooleanField(default=False)
    can_sponsors_see = models.BooleanField(default=True)

    @property
    def is_complete(self):
        return all(
            (
                self.university, self.university_degree, self.major,
                self.phone_number, self.birth_date, self.firstname_fa,
                self.lastname_fa, self.national_code
            )
        )

    @staticmethod
    def sensitive_fields():
        return ('hide_profile_info', 'can_sponsors_see', 'phone_number',
                'province', 'is_complete', 'national_code', 'resume', )

    def __str__(self):
        pass


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

