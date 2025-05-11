from django.contrib import admin
from .models import UserActivity

@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    list_display = ("session_key", "page_url", "event_type", "element_id", "scroll_depth", "duration", "timestamp")
    list_filter = ("event_type",)