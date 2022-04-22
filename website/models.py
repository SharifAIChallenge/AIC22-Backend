from django.db import models
from constants import SHORT_TEXT_MAX_LENGTH, URL_MAX_LENGTH,\
    MEDIUM_TEXT_MAX_LENGTH, LONG_TEXT_MAX_LENGTH


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


class FrequentlyAskedQuestions(models.Model):
    title = models.CharField(max_length=MEDIUM_TEXT_MAX_LENGTH)
    question_en = models.CharField(max_length=LONG_TEXT_MAX_LENGTH)
    question_fa = models.CharField(max_length=LONG_TEXT_MAX_LENGTH)
    answer_en = models.CharField(max_length=LONG_TEXT_MAX_LENGTH)
    answer_fa = models.CharField(max_length=LONG_TEXT_MAX_LENGTH)
