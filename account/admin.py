from django.contrib import admin

from import_export.admin import ImportExportModelAdmin
# Register your models here.
from account.models import User, Skill, JobExperience, MyProfile


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


@admin.register(MyProfile)
class ProfileAdmin(admin.ModelAdmin):
    pass


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    pass


@admin.register(JobExperience)
class JobExperienceAdmin(admin.ModelAdmin):
    pass
