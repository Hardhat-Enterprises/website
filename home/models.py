import uuid

from django.db.models.deletion import PROTECT
from django.db import models
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import gettext_lazy as _
from tinymce.models import HTMLField
from django.contrib.auth.models import User 


from django.utils.text import slugify

import secrets


from .mixins import AbstractBaseSet, CustomUserManager
from .validators import StudentIdValidator

class User(AbstractBaseUser, PermissionsMixin):
    """
    A User model with admin-compliant permissions.
    email and password are required. Other fields are optional.
    """

    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)
    email = models.EmailField(_("deakin email address"), blank=False, unique=True)
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
    created_at = models.DateTimeField(_("created_at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated_at"), auto_now=True)

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

#Search Bar Models:

class Webpage(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True)
    url = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    
    def __str__(self) -> str:
        return self.title


class Project(AbstractBaseSet):

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True)
    title = models.CharField(_("project title"), max_length=150, blank=True)

    def __str__(self) -> str:
        return self.title


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
    course = models.ForeignKey(Course, on_delete=PROTECT, related_name="course", blank=True, null=True)
    p1 = models.ForeignKey(Project, on_delete=PROTECT, related_name="p1", blank=False, null=False)
    p2 = models.ForeignKey(Project, on_delete=PROTECT, related_name="p2", blank=False, null=False)
    p3 = models.ForeignKey(Project, on_delete=PROTECT, related_name="p3", blank=False, null=False)
    allocated = models.ForeignKey(Project, on_delete=PROTECT, related_name="allocated", blank=True, null=True)
    skills = models.ManyToManyField(Skill, through='Progress')
    
    def __str__(self) -> str:
        return str(self.user)

    

# class Skill(models.Model):
#     name = models.CharField(max_length=255)
#     description = models.TextField()
#     def __str__(self):
#         return self.name





class Contact(models.Model):
    name=models.CharField(max_length=100)
    email=models.CharField(max_length=200)
    message=models.TextField(max_length=1000)
    
    def __str__(self):
        return self.name

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

class Article(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    featured = models.BooleanField(default=False)
    likes = models.ManyToManyField(User, related_name='liked_articles', blank=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    article = models.ForeignKey(Article, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user.username}'

class Smishingdetection_join_us(models.Model):
    name= models.CharField(max_length=100)
    email= models.CharField(max_length=200)
    message= models.TextField(max_length=1000)

class Projects_join_us(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=200)
    message = models.TextField(max_length=1000)
    page_name = models.CharField(max_length=100)


class Document(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
