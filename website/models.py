from django.db import models
from constants import SHORT_TEXT_MAX_LENGTH, LONG_TEXT_MAX_LENGTH, URL_MAX_LENGTH, MEDIUM_TEXT_MAX_LENGTH


def staff_upload_path(instance, filename):
    return f'staff/{instance.team.group.title}/{instance.team.title}/{filename}'


def tweet_upload_path(instance, filename):
    return f'tweet/{filename}'


class StaffGroup(models.Model):
    title = models.CharField(max_length=SHORT_TEXT_MAX_LENGTH)

    def __str__(self):
        return self.title


class StaffTeam(models.Model):
    title = models.CharField(max_length=SHORT_TEXT_MAX_LENGTH)
    group = models.ForeignKey(StaffGroup, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Staff(models.Model):
    team = models.ForeignKey(StaffTeam, on_delete=models.SET_NULL, null=True, blank=True)
    first_name_en = models.CharField(max_length=SHORT_TEXT_MAX_LENGTH, null=True, blank=True)
    first_name_fa = models.CharField(max_length=SHORT_TEXT_MAX_LENGTH)
    last_name_en = models.CharField(max_length=SHORT_TEXT_MAX_LENGTH, null=True, blank=True)
    last_name_fa = models.CharField(max_length=SHORT_TEXT_MAX_LENGTH)
    role = models.CharField(max_length=SHORT_TEXT_MAX_LENGTH, blank=True, null=False)
    url = models.CharField(max_length=URL_MAX_LENGTH, null=True, blank=True)
    image = models.ImageField(upload_to=staff_upload_path)

    def __str__(self):
        return "%s %s" % (self.first_name_en, self.last_name_en)


class Tweet(models.Model):
    author = models.CharField(max_length=SHORT_TEXT_MAX_LENGTH, null=True)
    text = models.TextField(max_length=LONG_TEXT_MAX_LENGTH, null=True)
    image = models.ImageField(null=True, upload_to=tweet_upload_path)
    post_time = models.DateTimeField(null=True)
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
    description_fa = models.TextField(max_length=LONG_TEXT_MAX_LENGTH, null=True)


class FrequentlyAskedQuestions(models.Model):
    title = models.CharField(max_length=MEDIUM_TEXT_MAX_LENGTH)
    question_en = models.CharField(max_length=LONG_TEXT_MAX_LENGTH)
    question_fa = models.CharField(max_length=LONG_TEXT_MAX_LENGTH)
    answer_en = models.CharField(max_length=LONG_TEXT_MAX_LENGTH)
    answer_fa = models.CharField(max_length=LONG_TEXT_MAX_LENGTH)
    show_on_landing_page = models.BooleanField(default=False)


class News(models.Model):
    title = models.CharField(max_length=MEDIUM_TEXT_MAX_LENGTH)
    preview = models.TextField(max_length=LONG_TEXT_MAX_LENGTH, null=True, blank=True)
    body = models.TextField(max_length=LONG_TEXT_MAX_LENGTH, null=True, blank=True)
    post_time = models.DateTimeField(null=True)
    importance = models.PositiveSmallIntegerField(default=0)


class NewsTag(models.Model):
    title = models.CharField(max_length=SHORT_TEXT_MAX_LENGTH)

    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='tags')


class TimelineEvent(models.Model):
    date = models.DateTimeField(null=True, blank=True)
    title_en = models.CharField(max_length=SHORT_TEXT_MAX_LENGTH)
    title_fa = models.CharField(max_length=SHORT_TEXT_MAX_LENGTH)
    text_en = models.TextField()
    text_fa = models.TextField()

    day = models.CharField(max_length=SHORT_TEXT_MAX_LENGTH, null=True, blank=True)
    month = models.CharField(max_length=SHORT_TEXT_MAX_LENGTH, null=True, blank=True)

    order = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return self.title_en


class Statistic(models.Model):
    value = models.IntegerField(default=0)
    title = models.CharField(max_length=SHORT_TEXT_MAX_LENGTH)
    title_fa = models.CharField(max_length=SHORT_TEXT_MAX_LENGTH)


class UTMTracker(models.Model):
    title = models.CharField(max_length=SHORT_TEXT_MAX_LENGTH, null=True, blank=True)
    count = models.IntegerField(default=0)
    code = models.CharField(max_length=4, null=False, blank=False)

    def increase(self):
        self.count += 1
        self.save()
