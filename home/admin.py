from django.contrib import admin
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
    LeaderBoardTable

)



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
    list_display = ['title', 'difficulty', 'category', 'points']

@admin.register(UserChallenge)
class UserChallengeAdmin(admin.ModelAdmin):
    list_display = ['user', 'challenge', 'completed', 'score']


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


from .models import CodePuzzle 

@admin.register(CodePuzzle)
class CodePuzzleAdmin(admin.ModelAdmin):
    list_display = ['title', 'difficulty', 'challenge_type']
    search_fields = ['title', 'description']
    list_filter = ['difficulty', 'challenge_type']
    fields = [
        'title', 'description', 'difficulty',
        'input_description', 'sample_input', 'sample_output',
        'expected_output', 'correct_answer',
        'starter_code', 'challenge_type'  # newly added fields
    ]


from .models import Submission

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ['user', 'puzzle', 'is_correct', 'submitted_at']
    list_filter = ['is_correct', 'submitted_at']
    search_fields = ['user__username', 'puzzle__title']


