import csv

from django.contrib import admin
from django.http import HttpResponse

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
    actions = ["export_as_csv"]

    def export_as_csv(self, request, queryset):
        meta = Profile._meta
        field_names = [field.name for field in meta.fields]
        field_names += ['team', 'email']
        print(len(field_names))

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            data = [getattr(obj, field) for field in field_names[:21]]
            data += [obj.user.team.name if obj.user.team is not None else ""]
            data += [obj.user.email]
            row = writer.writerow(data)

        return response

    export_as_csv.short_description = "Export Selected"


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    pass


@admin.register(JobExperience)
class JobExperienceAdmin(admin.ModelAdmin):
    pass


@admin.register(ProgrammingLanguage)
class ProgrammingLanguageAdmin(admin.ModelAdmin):
    pass
