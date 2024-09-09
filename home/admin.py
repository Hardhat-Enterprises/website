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

    
    # Contact_central,
    Article,
    Smishingdetection_join_us,
    Projects_join_us,

    # Logging
    SecurityEvent

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
    
    
# @admin.register(Contact_central)
# class Contact_centralAdmin(admin.ModelAdmin):
#     list_display = [field.name for field in Contact_central._meta.fields]

# class OtpTokenAdmin(admin.ModelAdmin):
#     list_display = ("user", "otp_code")

#admin.site.register(OtpToken, OtpTokenAdmin)
admin.site.register(Projects_join_us)





