from django.contrib import admin

# Register your models here.
from account.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', ]
    # list_editable = []
    # list_display_links = []
    # search_fields = []
    # sortable_by = []
    # list_filter = []
