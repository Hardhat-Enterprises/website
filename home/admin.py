from django.contrib import admin
from .models import (
    User,
    Student,
    Project
)

admin.site.site_header = "Hardhat Enterprises Administration"
admin.site.site_title = "Hardhat Admin Portal"
admin.site.index_title = "Welcome to Hardhat Admin Portal"

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [field.name for field in User._meta.fields]

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Student._meta.fields]

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Project._meta.fields]
