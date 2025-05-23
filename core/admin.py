from django.contrib import admin
from .models import BlacklistedIP

@admin.register(BlacklistedIP)
class BlacklistedIPAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'is_blacklisted', 'created_at')
