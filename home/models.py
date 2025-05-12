import uuid

from django.db.models.deletion import PROTECT
from django.db import models
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser  
from django.contrib.auth.models import BaseUserManager
from django.contrib.sessions.models import Session

from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from tinymce.models import HTMLField


from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.utils.timezone import now
from django.utils.text import slugify

import secrets
import random
import string

from .mixins import AbstractBaseSet, CustomUserManager
from .validators import StudentIdValidator
from django.db import models

import nh3

class APIModel(models.Model):
    name = models.CharField(max_length=255)
    field_name = models.CharField(max_length=255, default="Default Value")
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
   
    def __str__(self):
        return self.field_name
    
class User(AbstractBaseUser, PermissionsMixin):
    """
    A User model with admin-compliant permissions.
    email and password are required. Other fields are optional.
    """

    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)
    email = models.EmailField(_("deakin email address"), blank=False, unique=True)
    upskilling_progress = models.JSONField(default=dict, blank=True, null=True)

    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    is_verified = models.BooleanField(
        _("verified"),
        default=False,
        help_text=_("Designates whether the user has verified their account."),
    )
    created_at = models.DateTimeField(_("created_at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated_at"), auto_now=True)
    
    last_activity = models.DateTimeField(null=True, blank=True, default=now)


    current_session_key = models.CharField(max_length=40, null=True, blank=True)

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"

    objects = CustomUserManager()

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self):
        return self.get_full_name()

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)
    def activate_user(self):
        """ Mark the user as verified and active."""
        self.is_verified = True
        self.is_active = True
        self.save()
        print(f"User {self.email} has been activated and verified.")
    
    def generate_passkeys(self):
        """Generate 5 unique passkeys for the user after email verification."""
        from home.models import Passkey 

        if self.passkeys.count() < 5:
            for _ in range(5):
                new_key = Passkey.generate_passkey()
                Passkey.objects.create(user=self, key=new_key)

    def update_last_activity(self, request):
        #Updates user last activity with timestamp
        if not request.session.session_key:
            request.session.save()
        self.last_activity = now()
        self.current_session_key = request.session.session_key
        self.save(update_fields=['last_activity', 'current_session_key'])

#Search Bar Models:

class Webpage(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True)
    url = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    
    def __str__(self) -> str:
        return self.title


class Project(AbstractBaseSet):

    PROJECT_CHOICES = [
        ('AppAttack', 'AppAttack'),
        ('Malware', 'Malware'),
        ('PT-GUI', 'PT-GUI'),
        ('Smishing_Detection', 'Smishing Detection'),
        ('Deakin_CyberSafe_VR', 'Deakin CyberSafe VR'),
        ('Deakin_Threat_Mirror', 'Deakin Threat Mirror'),
        ('Company_Website_Development', 'Company Website Development'),
    ]

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True)
    title = models.CharField(_("project title"), max_length=150, choices=PROJECT_CHOICES, blank=False)

    def __str__(self) -> str:
        return self.get_title_display()


class Course(AbstractBaseSet):

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True)
    title = models.CharField(_("course title"), max_length=150, blank=True)
    code = models.CharField(_("course code"), max_length=150, blank=True)
    is_postgraduate = models.BooleanField(_("postgraduate status"), default=False)

    def __str__(self):
        return self.title

class Skill(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    slug = models.SlugField(blank=True)

    def __str__(self):
        return self.name

class Student(AbstractBaseSet):

    T1 = 'T1'
    T2 = 'T2'
    T3 = 'T3'
    TRIMESTERS = [
        (T1, 'Trimester 1'),
        (T2, 'Trimester 2'),
        (T3, 'Trimester 3'),
    ]

    SIT782 = 'SIT782'
    SIT764 = 'SIT764'
    SIT378 = 'SIT378'
    SIT374 = 'SIT374'
    UNITS = [
        (SIT782, 'SIT782'),
        (SIT764, 'SIT764'),
        (SIT378, 'SIT378'),
        (SIT374, 'SIT374'),
    ]

    COURSES = [
        ('BDS', 'Bachelor of Data Science'),
        ('BCS', 'Bachelor of Computer Science'),
        ('BCYB', 'Bachelor of Cyber Security'),
        ('BIT', 'Bachelor of Information Technology'),
        ('BSE', 'Bachelor of Software Enginerring'),
        ('BAI', 'Bachelor of AI'),
        ('MAAI', 'Master of Applied AI'),
        ('MDS', 'Master of Data Science'),
        ('MIT', 'Master of Information Technology'),
        ('MITM', 'Master of IT Management'),
        ('MCS', 'Master of Cyber Security')

    ]


    student_id_validator = StudentIdValidator()

    id = models.BigIntegerField(
        _("student_id"),
        primary_key=True,
        unique=True,
        help_text=_("Required. Enter Deakin Student ID. Digits only."),
        validators=[StudentIdValidator],
        error_messages={
            "unique": _("A user with that Student ID already exists."),
        },
    )
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=PROTECT, related_name="users", blank=False, null=False)
    year = models.PositiveIntegerField(blank=True)
    trimester = models.CharField(_("trimester"), choices=TRIMESTERS, max_length=10, blank=True)
    unit = models.CharField(_("unit"), choices=UNITS, max_length=50, blank=True)
    course = models.CharField(max_length=10, choices=COURSES, blank=True, null=True)
    p1 = models.ForeignKey(Project, on_delete=models.PROTECT, related_name="p1_preferences", null=True, blank=True)
    p2 = models.ForeignKey(Project, on_delete=models.PROTECT, related_name="p2_preferences", null=True, blank=True)
    p3 = models.ForeignKey(Project, on_delete=models.PROTECT, related_name="p3_preferences", null=True, blank=True)

    def clean(self):
        if self.p1 == self.p2 or self.p1 == self.p3 or self.p2 == self.p3:
            raise ValidationError("Project preferences p1, p2, and p3 must be unique.")
    allocated = models.ForeignKey(Project, on_delete=PROTECT, related_name="allocated", blank=True, null=True)
    skills = models.ManyToManyField(Skill, through='Progress')
    
    def __str__(self) -> str:
        return str(self.user)

    

# class Skill(models.Model):
#     name = models.CharField(max_length=255)
#     description = models.TextField()
#     def __str__(self):
#         return self.name




#Contact Model
class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=200)
    message = models.TextField(max_length=1000)

    def save(self, *args, **kwargs):
        self.name = nh3.clean(self.name, tags=set(), attributes={}, link_rel=None)
        self.message = nh3.clean(self.message, tags=set(), attributes={}, link_rel=None)
        super(Contact, self).save(*args, **kwargs)

class DDT_contact(models.Model):
    fullname=models.CharField(max_length=100)
    email=models.CharField(max_length=200)
    mobile=models.CharField(max_length=200)
    message=models.TextField(max_length=1000)
    
    def __str__(self):
        return self.fullname
    class Meta:
        verbose_name = "DDT_contact"
        verbose_name_plural = "DDT_contact"
    

# class Contact_central(models.Model):
#     name=models.CharField(max_length=100)
#     email=models.CharField(max_length=200)
#     message=models.TextField(max_length=1000)

#     def __str__(self):
#         return self.name


class Progress(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    skill = models.ForeignKey('Skill', on_delete=models.CASCADE)
    progress = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('student', 'skill')

    def __str__(self):

        return f'{self.student} - {self.skill.name}: {self.progress}%'

        return f'{self.student} - {self.skill}: {"Completed" if self.completed else "Not completed"}'



class Article(models.Model):
    title = models.CharField(max_length=255)
    content = HTMLField()
    date = models.DateField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    featured = models.BooleanField(default=False)
    likes = models.ManyToManyField(User, related_name='likes', blank=True)



class Smishingdetection_join_us(models.Model):
    name= models.CharField(max_length=100)
    email= models.CharField(max_length=200)
    message= models.TextField(max_length=1000)

class Projects_join_us(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=200)
    message = models.TextField(max_length=1000)
    page_name = models.CharField(max_length=100)

#class Feedback(models.Model):
#    name = models.CharField(max_length=100)
#    feedback = models.TextField()
#    rating = models.CharField(max_length=20)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True, null=True)
    linkedin = models.URLField(max_length=200, blank=True, null=True)
    github = models.URLField(max_length=200, blank=True, null=True)
    # phone = models.CharField(max_length=20, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.user.username

    
class CyberChallenge(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]
    CATEGORY_CHOICES = [
        ('network', 'Network Security'),
        ('web', 'Web Application Security'),
        ('crypto', 'Cryptography'),
        ('general', 'General Knowledge'),
        ('python', 'Python'),
        ('javascript', 'JavaScript'),
        ('html_css', 'HTML & CSS'),
        ('web_security', 'Web Security'),
        ('reverse_engineering', 'Reverse Engineering'),
        ('forensics', 'Forensics'),
        ('binary_exploitation', 'Binary Exploitation'),
        ('linux', 'Linux'),
        ('algorithms', 'Algorithms'),
        ('data_structures', 'Data Structures'),
        ('databases', 'Databases'),
        ('regex', 'Regex'),
        ('secure_coding', 'Secure Coding'),
        ('logic_reasoning', 'Logic & Reasoning'),
        ('misc', 'Miscellaneous'),
    ]
    
    title = models.CharField(max_length=255)
    description = models.TextField()
    question = models.TextField(blank=True, null=True, default="")
    choices = models.JSONField(blank=True, null=True)  # For MCQ challenges
    correct_answer = models.CharField(max_length=200, blank=True, null=True)  # Correct answer for MCQs or expected output for code challenges
    starter_code = models.TextField(blank=True, null=True)  # For Fix the Code challenges
    sample_input = models.TextField(blank=True, null=True)  # For Fix the Code challenges
    expected_output = models.TextField(blank=True, null=True)  # For Fix the Code challenges
    explanation = models.TextField(blank=True, null=True, default="")
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    points = models.IntegerField(default=10)
    challenge_type = models.CharField(max_length=20, choices=[('mcq', 'Multiple Choice'), ('fix_code', 'Fix the Code')])
    time_limit = models.IntegerField(default=60)  

    def __str__(self):
        return self.title


class UserChallenge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    challenge = models.ForeignKey(CyberChallenge, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    score = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} - {self.challenge.title}"



class BlogPost(models.Model): 
    title = models.CharField(max_length=255)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    page_name = models.CharField(max_length=100)

    def __str__(self):
        return self.title

    


    User = get_user_model()

#class Feedback(models.Model):
    #GENERAL_INQUIRY = 'general'
    #BUG = 'bug'
    #IMPROVEMENT = 'improvement'
    #FEATURE_REQUEST = 'feature'

    #FEEDBACK_TYPES = [
    #    (GENERAL_INQUIRY, 'General Inquiry'),
    #    (BUG, 'Bug Report'),
    #    (IMPROVEMENT, 'Improvement Suggestion'),
    #    (FEATURE_REQUEST, 'Request for a Feature')
    #]

    #user = models.ForeignKey(
    #    User,
    #    on_delete=models.CASCADE,
    #    null=True,
    #    blank=True,
    #)
    #feedback_type = models.CharField(
    #    max_length=20,
    #    choices=FEEDBACK_TYPES,
    #)
    #content = models.TextField()
    #created_at = models.DateTimeField(auto_now_add=True)

    #def __str__(self):
        #feedback_type_display = self.get_feedback_type_display()
        #return f"{feedback_type_display} - {self.created_at}"

class Announcement(models.Model):
    message = models.TextField()
    isActive = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)


class SecurityEvent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    event_type = models.CharField(max_length=50)  # e.g., 'login_success', 'login_failure'
    ip_address = models.GenericIPAddressField()
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.TextField(blank=True)

    def __str__(self):
        return f"{self.event_type} - {self.user or 'Unknown user'} - {self.timestamp}"


class ExampleModel(models.Model):
    name = models.CharField(max_length=255)  
    updated_at = models.DateTimeField(auto_now=True)  # Automatically updates the timestamp on save

    def __str__(self):
      
        feedback_type_display = self.get_feedback_type_display()
        return f"{feedback_type_display} - {self.created_at}"
    

class ContactSubmission(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"

        return self.name

class Job(models.Model):
    title = models.CharField(max_length=200)
    description = HTMLField()
    location = models.CharField(max_length=100,choices=[("Remote","Remote"),("OnSite","OnSite")])
    job_type = models.CharField(max_length=50, choices=[('FT', 'Full-time'), ('PT', 'Part-time'), ('CT', 'Contract')])
    posted_date = models.DateField(auto_now_add=True)
    closing_date = models.DateField()

    def __str__(self):
        return self.title
    
class JobApplication(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="applications")
    name = models.CharField(max_length=100)
    email = models.EmailField()
    resume = models.FileField(upload_to="resumes/")
    cover_letter = models.FileField(upload_to="cover_letter/")
    applied_date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.name} - {self.job.title}"

#Leaderboard
class LeaderBoardTable(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=200)
    total_points = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-total_points']  

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} ({self.category}) - {self.total_points} POINTS"
class Experience(models.Model):
    name = models.CharField(max_length=100)
    feedback = models.TextField()
    rating = models.IntegerField(null=True, blank=True)  # ⭐ ADDED THIS LINE
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.feedback[:50]}"

class Passkey(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="passkeys")
    key = models.CharField(max_length=12, unique=True)
    created_at = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return f"Passkey for {self.user.email}"

    @staticmethod
    def generate_passkey():
        """Generate a new passkey"""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=12))

class AppAttackReport(models.Model):
    year = models.PositiveIntegerField()
    title = models.CharField(max_length=255)
    pdf = models.FileField(upload_to='appattack/reports/')

    def __str__(self):
        return f"{self.year} - {self.title}"


class PenTestingRequest(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    github_repo_link = models.URLField()
    project_description = models.TextField(blank=True)
    terms_accepted = models.BooleanField(default=False)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - PenTesting Request"


class SecureCodeReviewRequest(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    github_repo_link = models.URLField()
    project_description = models.TextField(blank=True)
    terms_accepted = models.BooleanField(default=False)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - Secure Code Review Request"

