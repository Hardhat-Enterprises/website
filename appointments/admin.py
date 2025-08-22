from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Counsellor, Appointment

@admin.register(Counsellor)
class CounsellorAdmin(admin.ModelAdmin):
    list_display = ("name", "title", "email", "is_active")
    list_filter = ("is_active",)

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("date", "time", "counsellor", "full_name", "status", "created_at")
    list_filter = ("status", "counsellor", "date")
    search_fields = ("full_name", "email", "phone", "notes")
