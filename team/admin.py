from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.db import models

from martor.widgets import AdminMartorWidget

from .models import Team, Invitation


class InvitationInline(admin.StackedInline):
    model = Invitation


@admin.register(Team)
class TeamAdmin(ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': AdminMartorWidget},
    }
    list_display = ('id', 'name', 'image', 'creator', 'is_finalist', )
    search_fields = ('name',)
    list_editable = ('name', 'image', 'is_finalist')
    list_filter = ('is_finalist', )
    inlines = (InvitationInline, )


@admin.register(Invitation)
class InvitationAdmin(ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': AdminMartorWidget},
    }
    list_display = ('id', 'user', 'team', 'type', 'status')
    list_filter = ('type', 'status')


