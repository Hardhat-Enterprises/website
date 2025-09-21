

from django.contrib import admin
from .models import TeamMember
from .models import AdminNotification
from .models import VaultDocument

from django.utils.html import format_html

# from .models import Resource  # Not needed for cyber challenge/quiz/compiler features

from .models import Tip , TipRotationState
from .models import (
    User,
    Student,
    Project,
    Course,
    Skill,
    Progress,
    Contact,
    ContactSubmission,
    Experience,
    UserBlogPage,

    Webpage,
    DDT_contact,
    #Feedback,
    Job,
    JobApplication,
    
    # Contact_central,
    Article,
    Smishingdetection_join_us,
    Projects_join_us,
    CyberChallenge,
    UserChallenge,
    Announcement,

    # Logging
    SecurityEvent,

    #LeaderBaord
    LeaderBoardTable,

    AppAttackReport, 
    PenTestingRequest, 
    SecureCodeReviewRequest,


    # Python Compiler Models
    CodeExecution,
    CodeTemplate,
    CodeSubmission,
    CompilerSettings,

    JobAlert,
    GraduateProgram,
    CareerFAQ


)



@admin.register(AdminNotification)
class AdminNotificationAdmin(admin.ModelAdmin):
    list_display = ('message', 'created_at', 'is_read', 'related_user')
    list_filter = ('is_read', 'created_at')
    search_fields = ('message',)

admin.site.register(Smishingdetection_join_us)
admin.site.register(Article)
admin.site.register(DDT_contact)
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

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'image', 'created_at')

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Course._meta.fields]
    
@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Skill._meta.fields]

@admin.register(Progress)
class ProgressAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Progress._meta.fields]

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Contact._meta.fields]

@admin.register(SecurityEvent)
class SecurityEventAdmin(admin.ModelAdmin):
    list_display = [field.name for field in SecurityEvent._meta.fields]
    
#Webpage Search Model
@admin.register(Webpage)
class Webpage(admin.ModelAdmin):
    list_display = [field.name for field in Webpage._meta.fields]


@admin.register(CyberChallenge)
class CyberChallengeAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'difficulty', 'challenge_type', 'points')
    list_filter = ('category', 'difficulty', 'challenge_type')
    search_fields = ('title', 'description', 'question')

    def get_fields(self, request, obj=None):
        fields = [
            'title', 'description', 'question', 'explanation', 'difficulty',
            'category', 'points', 'challenge_type', 'time_limit'
        ]

        if obj:
            if obj.challenge_type == 'mcq':
                fields += ['choices', 'correct_answer']
            elif obj.challenge_type == 'fix_code':
                fields += ['starter_code', 'sample_input', 'expected_output', 'correct_answer']
        else:
            fields += ['choices', 'correct_answer', 'starter_code', 'sample_input', 'expected_output']

        return fields



@admin.register(UserChallenge)
class UserChallengeAdmin(admin.ModelAdmin):
    list_display = ('user', 'challenge', 'completed', 'score')


@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email', 'message', 'created_at') 
    
@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ['message', 'isActive', 'created_at']
    list_filter = ['isActive', 'created_at']
    search_fields = ['message']
    readonly_fields = ['created_at']
    
@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ['name', 'feedback', 'created_at']
    search_fields = ['name', 'feedback']
    
@admin.register(UserBlogPage)
class UserBlogPageAdmin(admin.ModelAdmin):
    list_display = ['name', 'title', 'description', 'created_at']
    search_fields = ['name', 'title', 'description']
    readonly_fields = ['created_at']  # Make created_at read-only
    
# @admin.register(Contact_central)
# class Contact_centralAdmin(admin.ModelAdmin):
#     list_display = [field.name for field in Contact_central._meta.fields]

#Feedback page
#@admin.register(Feedback, FeedbackAdmin)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['feedback_type', 'user', 'created_at']
    list_filter = ['feedback_type', 'created_at']
    search_fields = ['content', 'user__email']
    readonly_fields = ['created_at']

    def get_readonly_fields(self, request, obj=None):
        if obj:  # If we are editing an existing object
            return ['user', 'feedback_type', 'content'] + self.readonly_fields
        return self.readonly_fields

#admin.site.register(Feedback, FeedbackAdmin)


# class OtpTokenAdmin(admin.ModelAdmin):
#     list_display = ("user", "otp_code")

#admin.site.register(OtpToken, OtpTokenAdmin)
admin.site.register(Projects_join_us)

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ['title', 'location', 'job_type', 'posted_date', 'closing_date']
    list_filter=['location','job_type']

@admin.register(JobAlert)
class JobAlertAdmin(admin.ModelAdmin):
    list_display = ['email', 'is_active', 'created_at', 'last_notification']
    list_filter = ['is_active', 'created_at']
    search_fields = ['email']
    readonly_fields = ['created_at', 'last_notification']

@admin.register(GraduateProgram)
class GraduateProgramAdmin(admin.ModelAdmin):
    list_display = ['title', 'program_type', 'duration_months', 'start_date', 'application_deadline', 'is_active']
    list_filter = ['program_type', 'is_active', 'start_date', 'application_deadline']
    search_fields = ['title', 'description']
    readonly_fields = ['created_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'program_type', 'duration_months', 'start_date', 'application_deadline', 'is_active')
        }),
        ('Program Details', {
            'fields': ('overview', 'curriculum', 'benefits', 'requirements', 'application_process')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

@admin.register(CareerFAQ)
class CareerFAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'category', 'is_popular', 'order', 'created_at']
    list_filter = ['category', 'is_popular', 'created_at']
    search_fields = ['question', 'answer']
    list_editable = ['order', 'is_popular']
    readonly_fields = ['created_at']

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display=['name', 'email','job__title','applied_date']
    list_filter = ['job__title']
    readonly_fields =['job','name','email','resume','cover_letter','applied_date']
    
    @admin.display(description="Job Title")
    def job__title(self,obj):
        return obj.job.title
    
@admin.register(LeaderBoardTable)
class LeaderboardTableAdmin(admin.ModelAdmin):
    list_display = ('user', 'category', 'total_points')




@admin.register(AppAttackReport)
class AppAttackReportAdmin(admin.ModelAdmin):
    list_display = ('year', 'title', 'pdf_link')

    def pdf_link(self, obj):
        return format_html("<a href='{}' target='_blank'>View PDF</a>", obj.pdf.url)
    pdf_link.short_description = "PDF"


@admin.register(PenTestingRequest)
class PenTestingRequestAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'github_repo_link', 'submitted_at']
    list_filter = ['submitted_at']
    search_fields = ['name', 'email', 'github_repo_link']
    readonly_fields = ['submitted_at']


@admin.register(SecureCodeReviewRequest)
class SecureCodeReviewRequestAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'github_repo_link', 'submitted_at']
    list_filter = ['submitted_at']
    search_fields = ['name', 'email', 'github_repo_link']
    readonly_fields = ['submitted_at']


# Python Compiler Admin Classes
@admin.register(CodeExecution)
class CodeExecutionAdmin(admin.ModelAdmin):
    list_display = ['user', 'language', 'is_successful', 'execution_time', 'created_at', 'ip_address']
    list_filter = ['language', 'is_successful', 'created_at', 'ip_address']
    search_fields = ['user__email', 'code', 'output', 'error_message']
    readonly_fields = ['created_at', 'execution_time', 'memory_used']
    ordering = ['-created_at']
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # If editing existing object
            return ['user', 'language', 'code', 'input_data', 'output', 'error_message', 
                   'execution_time', 'memory_used', 'is_successful', 'created_at', 'ip_address']
        return self.readonly_fields


@admin.register(CodeTemplate)
class CodeTemplateAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'difficulty', 'is_active', 'created_at']
    list_filter = ['category', 'difficulty', 'is_active', 'created_at']
    search_fields = ['title', 'description', 'template_code']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'category', 'difficulty', 'is_active')
        }),
        ('Code Content', {
            'fields': ('template_code', 'expected_output', 'hints')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(CodeSubmission)
class CodeSubmissionAdmin(admin.ModelAdmin):
    list_display = ['user', 'template', 'is_correct', 'execution_time', 'submitted_at']
    list_filter = ['is_correct', 'submitted_at', 'template__category', 'template__difficulty']
    search_fields = ['user__email', 'template__title', 'user_code']
    readonly_fields = ['submitted_at', 'execution_time']
    ordering = ['-submitted_at']
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # If editing existing object
            return ['user', 'template', 'user_code', 'is_correct', 'execution_time', 'submitted_at']
        return self.readonly_fields


@admin.register(CompilerSettings)
class CompilerSettingsAdmin(admin.ModelAdmin):
    list_display = ['max_execution_time', 'max_memory_limit', 'max_code_length', 'is_active', 'updated_at']
    list_filter = ['is_active', 'created_at', 'updated_at']
    readonly_fields = ['created_at', 'updated_at']
    
    def has_add_permission(self, request):
        # Only allow one settings instance
        return not CompilerSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Prevent deletion of settings
        return False

# Resource admin registration removed - not part of cyber challenge/quiz/compiler features
# @admin.register(Resource)
# class ResourceAdmin(admin.ModelAdmin):
#     list_display = ("title", "category", "is_published", "published_at")
#     list_filter = ("category", "is_published")
#     search_fields = ("title", "summary")
#     prepopulated_fields = {"slug": ("title",)}




@admin.register(Tip)
class TipAdmin(admin.ModelAdmin):
    list_display = ("text", "is_active", "created_at")
    list_filter = ("is_active",)
    search_fields = ("text",)

@admin.register(TipRotationState)
class TipRotationStateAdmin(admin.ModelAdmin):
    list_display = ("lock", "last_index", "rotated_at")

@admin.register(VaultDocument)
class VaultDocumentAdmin(admin.ModelAdmin):
    list_display = ('original_name', 'uploaded_by', 'content_type', 'size_bytes', 'created_at')
    search_fields = ('original_name', 'description')

# Resource registration completely removed - not part of cyber challenge/quiz/compiler features


