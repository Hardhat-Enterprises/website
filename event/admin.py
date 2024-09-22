from django.contrib import admin

from .models import VisitorLog, UserClickEvent

# Register your models here.


class VisitorLogAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'email', 'page_url', 'timestamp')
    list_filter = ('user', 'timestamp')
    search_fields = ('ip_address', 'page_url')
    readonly_fields = ('ip_address', 'user', 'page_url', 'timestamp')
    ordering = ('-timestamp',)

    @admin.display(description="email")
    def email(self, obj):
        if obj.user:
            return obj.user.email

class UserClickEventAdmin(admin.ModelAdmin):
    list_display = ('email', 'page_url', 'clicked_element', 'click_time')
    list_filter = ('user', 'click_time')
    search_fields = ('user__email', 'page_url', 'clicked_element')
    readonly_fields = ('user', 'page_url', 'clicked_element', 'click_time')
    ordering = ('-click_time',)

    @admin.display(description="email")
    def email(self, obj):
        if obj.user:
            return obj.user.email


admin.site.register(VisitorLog, VisitorLogAdmin)
admin.site.register(UserClickEvent, UserClickEventAdmin)
