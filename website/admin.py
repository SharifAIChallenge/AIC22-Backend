from django.contrib import admin
from .models import Staff, Tweet, Prize, PastAIC, FrequentlyAskedQuestions, News, NewsTag


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ['id', 'group_title', 'team_title', 'first_name_fa', 'last_name_fa', ]
    list_editable = ['group_title', 'team_title', 'first_name_fa', 'last_name_fa', ]
    list_display_links = ['id', ]
    search_fields = ['group_title', 'team_title', 'first_name_en', 'last_name_en', ]
    sortable_by = ['id', 'group_title', 'team_title', 'first_name_en', 'last_name_en', ]
    list_filter = ['group_title', 'team_title', ]


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
                    'answer_en', 'answer_fa']
    list_editable = ['title', 'question_en', 'question_fa',
                     'answer_en', 'answer_fa']
    list_display_links = ['id']
    sortable_by = ['id', 'title', 'question_en', 'question_fa',
                   'answer_en', 'answer_fa']
    search_fields = ['title', 'question_en', 'question_fa',
                     'answer_en', 'answer_fa']


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    pass


@admin.register(NewsTag)
class NewsTagAdmin(admin.ModelAdmin):
    pass
