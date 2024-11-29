from django.contrib import admin
from .models import (
    User,
    Student,
    Project,
    Course,
    Skill,
    Progress,
    Contact,
    Webpage,
    DDT_contact,
    Feedback,
    Article,
    Smishingdetection_join_us,
    Projects_join_us,
    CyberChallenge,
    UserChallenge,
    Announcement,
    SecurityEvent,
)

# Customize Admin Panel Headers
admin.site.site_header = "Hardhat Enterprises Administration"
admin.site.site_title = "Hardhat Admin Portal"
admin.site.index_title = "Welcome to Hardhat Admin Portal"

# User Management Models
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [field.name for field in User._meta.fields]

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Student._meta.fields]

# Project Management Models
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Project._meta.fields]

@admin.register(Projects_join_us)
class ProjectsJoinUsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Projects_join_us._meta.fields]

# Course and Skill Models
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Course._meta.fields]

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Skill._meta.fields]

@admin.register(Progress)
class ProgressAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Progress._meta.fields]

# Contact Models
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Contact._meta.fields]

@admin.register(DDT_contact)
class DDTContactAdmin(admin.ModelAdmin):
    list_display = [field.name for field in DDT_contact._meta.fields]

# Security Event Model
@admin.register(SecurityEvent)
class SecurityEventAdmin(admin.ModelAdmin):
    list_display = [field.name for field in SecurityEvent._meta.fields]

# Webpage Management
@admin.register(Webpage)
class WebpageAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Webpage._meta.fields]

# Feedback Model
@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['feedback_type', 'user', 'created_at']
    list_filter = ['feedback_type', 'created_at']
    search_fields = ['content', 'user__email']
    readonly_fields = ['created_at']

    def get_readonly_fields(self, request, obj=None):
        if obj:  # If editing an existing object
            return ['user', 'feedback_type', 'content'] + self.readonly_fields
        return self.readonly_fields

# Article Management
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Article._meta.fields]

# Smishing Detection
@admin.register(Smishingdetection_join_us)
class SmishingDetectionAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Smishingdetection_join_us._meta.fields]

# Cyber Challenges
@admin.register(CyberChallenge)
class CyberChallengeAdmin(admin.ModelAdmin):
    list_display = ['title', 'difficulty', 'category', 'points']

@admin.register(UserChallenge)
class UserChallengeAdmin(admin.ModelAdmin):
    list_display = ['user', 'challenge', 'completed', 'score']

# Announcements
@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ['message', 'isActive', 'created_at']
    list_filter = ['isActive', 'created_at']
    search_fields = ['message']
    readonly_fields = ['created_at']
