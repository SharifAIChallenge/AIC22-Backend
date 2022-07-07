from django.contrib import admin

from account.models import User, Skill, JobExperience, Profile, ProgrammingLanguage


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', ]
    # list_editable = []
    # list_display_links = []
    # search_fields = []
    # sortable_by = []
    # list_filter = []


class SkillInline(admin.StackedInline):
    model = Skill


class JobExperienceInline(admin.StackedInline):
    model = JobExperience


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    pass


@admin.register(JobExperience)
class JobExperienceAdmin(admin.ModelAdmin):
    pass


@admin.register(ProgrammingLanguage)
class ProgrammingLanguageAdmin(admin.ModelAdmin):
    pass
