from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import Tag, Ticket, Reply


class ReplyInline(admin.StackedInline):
    model = Reply


@admin.register(Ticket)
class TicketAdmin(ModelAdmin):
    pass


@admin.register(Reply)
class ReplyAdmin(ModelAdmin):
    pass


@admin.register(Tag)
class TagAdmin(ModelAdmin):
    pass
