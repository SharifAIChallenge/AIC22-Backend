from django.contrib import admin
from .models import (Staff, TimelineEvent, Tweet, Prize, PastAIC, FrequentlyAskedQuestions, News, NewsTag,
                     StaffTeam, StaffGroup, Statistic, UTMTracker)


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    pass


@admin.register(StaffTeam)
class StaffTeamAdmin(admin.ModelAdmin):
    pass


@admin.register(StaffGroup)
class StaffGroupAdmin(admin.ModelAdmin):
    pass


@admin.register(Tweet)
class TweetAdmin(admin.ModelAdmin):
    pass


@admin.register(Prize)
class PrizeAdmin(admin.ModelAdmin):
    pass


@admin.register(PastAIC)
class PastAICAdmin(admin.ModelAdmin):
    pass


@admin.register(FrequentlyAskedQuestions)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'question_en', 'question_fa',
                    'answer_en', 'answer_fa', 'show_on_landing_page']
    list_editable = ['title', 'question_en', 'question_fa',
                     'answer_en', 'answer_fa', 'show_on_landing_page']
    list_display_links = ['id']
    sortable_by = ['id', 'title', 'question_en', 'question_fa',
                   'answer_en', 'answer_fa', 'show_on_landing_page']
    search_fields = ['title', 'question_en', 'question_fa',
                     'answer_en', 'answer_fa', 'show_on_landing_page']


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    pass


@admin.register(NewsTag)
class NewsTagAdmin(admin.ModelAdmin):
    pass


@admin.register(TimelineEvent)
class TimelineEventAdmin(admin.ModelAdmin):
    pass


@admin.register(Statistic)
class StatisticAdmin(admin.ModelAdmin):
    pass


@admin.register(UTMTracker)
class UTMTrackerAdmin(admin.ModelAdmin):
    pass
