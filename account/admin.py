from django.contrib import admin

from import_export.admin import ImportExportModelAdmin

from .models import Profile, Skill, JobExperience


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
