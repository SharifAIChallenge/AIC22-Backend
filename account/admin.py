from django.contrib import admin

from import_export.admin import ImportExportModelAdmin
# Register your models here.
from account.models import User, Skill, JobExperience, Profile


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
class ProfileAdmin(ImportExportModelAdmin):
    inlines = (SkillInline, JobExperienceInline)
    list_display = ('id', 'firstname_fa', 'lastname_fa', 'birth_date', 'province',
                    'phone_number', 'national_code', 'university', 'major', 'university_degree')

    list_filter = ('university', 'major', 'university_degree')

    search_fields = ('firstname_fa', 'lastname_fa', 'major', 'province',
                     'phone_number', 'university', 'national_code')


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    pass


@admin.register(JobExperience)
class JobExperienceAdmin(admin.ModelAdmin):
    pass
