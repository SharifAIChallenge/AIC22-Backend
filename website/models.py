from django.db import models
from django.utils import timezone
from constants import SHORT_TEXT_MAX_LENGTH, LONG_TEXT_MAX_LENGTH, URL_MAX_LENGTH


def staff_upload_path(instance, filename):
    return f'staff/{instance.group_title}/{instance.team_title}/{filename}'


class Staff(models.Model):
    group_title = models.CharField(max_length=SHORT_TEXT_MAX_LENGTH)
    team_title = models.CharField(max_length=SHORT_TEXT_MAX_LENGTH, blank=True, null=True)
    first_name_en = models.CharField(max_length=SHORT_TEXT_MAX_LENGTH, null=True, blank=True)
    first_name_fa = models.CharField(max_length=SHORT_TEXT_MAX_LENGTH)
    last_name_en = models.CharField(max_length=SHORT_TEXT_MAX_LENGTH, null=True, blank=True)
    last_name_fa = models.CharField(max_length=SHORT_TEXT_MAX_LENGTH)
    role = models.CharField(max_length=SHORT_TEXT_MAX_LENGTH, blank=True, null=False)
    url = models.CharField(max_length=URL_MAX_LENGTH, null=True, blank=True)
    image = models.ImageField(upload_to=staff_upload_path)


class Tweet(models.Model):
    name = models.CharField(max_length=SHORT_TEXT_MAX_LENGTH)
    text = models.TextField(max_length=LONG_TEXT_MAX_LENGTH)
    image = models.ImageField(null=True, blank=True)
    create_time = models.DateTimeField(default=timezone.now)
    url = models.URLField(max_length=URL_MAX_LENGTH, null=True, blank=True)


class Prize(models.Model):
    title_en = models.CharField(max_length=SHORT_TEXT_MAX_LENGTH)
    title_fa = models.CharField(max_length=SHORT_TEXT_MAX_LENGTH)
    prize_en = models.CharField(max_length=SHORT_TEXT_MAX_LENGTH)
    prize_fa = models.CharField(max_length=SHORT_TEXT_MAX_LENGTH)
    team_name = models.CharField(max_length=SHORT_TEXT_MAX_LENGTH)


class PastAIC(models.Model):
    event_year = models.CharField(max_length=SHORT_TEXT_MAX_LENGTH)
    image = models.ImageField()
    title_en = models.CharField(max_length=SHORT_TEXT_MAX_LENGTH, blank=True)
    title_fa = models.CharField(max_length=SHORT_TEXT_MAX_LENGTH)
    description_en = models.TextField(max_length=LONG_TEXT_MAX_LENGTH, blank=True)
    description_fa = models.TextField(max_length=LONG_TEXT_MAX_LENGTH)
    firstTeam = models.TextField(max_length=SHORT_TEXT_MAX_LENGTH)
    secondTeam = models.TextField(max_length=SHORT_TEXT_MAX_LENGTH)
    thirdTeam = models.TextField(max_length=SHORT_TEXT_MAX_LENGTH)
