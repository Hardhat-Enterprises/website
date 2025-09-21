# from django.shortcuts import render, get_object_or_404
 
# views.py

from venv import logger
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404


from home.models import TeamMember
 

from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from textblob import TextBlob
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .forms import ExperienceForm
from .models import Experience
from django.db.models import Avg, Count

from django.db.models import Q
from django.views.generic import ListView
from .models import Resource
import mimetypes 

from .models import Tip, TipRotationState

from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import UserPassesTestMixin

from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetView, PasswordResetConfirmView, PasswordResetDoneView, PasswordResetCompleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
from django.db.models import Count, Q
from django.http import JsonResponse, HttpResponseNotAllowed
from django.contrib import messages
from django.views import View
from django.views.generic import ListView, DetailView, CreateView
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_protect
from .models import ContactSubmission
from django.utils.html import strip_tags
from .models import Report


from .models import Article, Student, Project, Contact, Smishingdetection_join_us, Projects_join_us, Webpage, Profile, User, Course, Skill, Experience, Job, JobAlert, UserBlogPage, VaultDocument #Feedback 


from django.contrib.auth import get_user_model
from .models import User
from django.utils import timezone
from django.core.mail import send_mail
from django.core.exceptions import ValidationError
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse_lazy
# from Website.settings import EMAIL_HOST_USER
import random
from .forms import UserUpdateForm, ProfileUpdateForm, ExperienceForm, JobApplicationForm, UserBlogPageForm, ChallengeForm, VaultUploadForm

from .forms import CaptchaForm

import os
import json
import bleach
import requests
import time
# from utils.charts import generate_color_palette
# from .models import Student, Project, Contact
from .forms import ClientRegistrationForm, RegistrationForm, UserLoginForm, ClientLoginForm, UserPasswordResetForm, UserPasswordChangeForm, UserSetPasswordForm, StudentForm, sd_JoinUsForm, projects_JoinUsForm, NewWebURL, Upskilling_JoinProjectForm


from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.views import LoginView
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator
from .forms import UserLoginForm
from django.core.cache import cache
from django.shortcuts import redirect
from django.urls import reverse
from home.models import Announcement, JobApplication
from django.http import Http404
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator

from pathlib import Path
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404
from django.utils.text import slugify

from datetime import timedelta

 

# import os
 
from .models import Smishingdetection_join_us, DDT_contact
# import json
 
 
# from utils.charts import generate_color_palette
# from .models import Student, Project, Contact
# from .forms import RegistrationForm, UserLoginForm, UserPasswordResetForm, UserPasswordChangeForm, UserSetPasswordForm, StudentForm, sd_JoinUsForm, NewWebURL
 
 

from utils.charts import generate_color_palette, colorPrimary, colorSuccess, colorDanger
from utils.passwords import gen_password
from .models import Student, Project, Progress, Skill, CyberChallenge, UserChallenge
from django.core.paginator import Paginator
from .models import BlogPost
from django.template.loader import render_to_string
import msal
import requests

#from .models import Student, Project, Progress
 
from .forms import FeedbackForm
import traceback

import string
import random

# from .forms import RegistrationForm, UserLoginForm, UserPasswordResetForm, UserPasswordChangeForm, UserSetPasswordForm, StudentForm
# Create your views here.

# Regular Views
def client_sign_in(request):
    return render(request, 'accounts/client_sign-in.html') 

#For Contact Form
import nh3
import logging
from .validators import xss_detection
from .models import Contact

from rest_framework.views import APIView
from rest_framework.response import Response
from .models import APIModel
from .serializers import APIModelSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.viewsets import ViewSet
from django.db.models import Count
from django.urls import reverse
from .models import CyberChallenge, UserChallenge



#For LeaderBoard
from django.db.models import Sum
from .models import LeaderBoardTable, UserChallenge
from django.contrib.auth.models import User

from .models import Passkey

from .forms import PenTestingRequestForm, SecureCodeReviewRequestForm
from .models import AppAttackReport


from home.models import TeamMember 

#For search form
import difflib
from django.utils.dateparse import parse_date
import re


def get_login_redirect_url(user):
    """
    Determine where to redirect user after login based on join-us completion status.
    If user hasn't completed join-us form, redirect to /join-us/
    If user has completed it, redirect to profile page
    """
    # TEMPORARY FIX: Always redirect to dashboard for OAuth users
    # This will be refined later to properly detect OAuth vs regular login
    print(f"DEBUG: get_login_redirect_url called for user: {user.email}")
    
    # For now, always redirect to dashboard to fix OAuth redirect issue
    print(f"DEBUG: get_login_redirect_url - Redirecting to dashboard")
    return '/dashboard/'
    
    # Original logic (commented out for now):
    # if Student.objects.filter(user=user).exists():
    #     # User has completed join-us form, redirect to profile
    #     return '/profile/'
    # else:
    #     # User hasn't completed join-us form, redirect to join-us page
    #     return '/join-us/'



def index(request):
    recent_announcement = Announcement.objects.filter(isActive=True).order_by('-created_at').first()
    max_age = 3600;
    
    if recent_announcement:
        has_cookies = request.COOKIES.get('announcement')
        if has_cookies:
            show_announcement = False
            announcement_message = recent_announcement.message
        else:
            show_announcement = recent_announcement.isActive
            announcement_message = recent_announcement.message   
    else:
        show_announcement = False
        announcement_message = "Welcome! Stay tuned for updates."
    
    response = render(
        request, 
        'pages/index.html', 
        {'announcement_message': announcement_message, 'show_announcement': show_announcement}
    )

    response.set_cookie('announcement', 'True', max_age=max_age)
    return response


def error_404_view(request,exception):
    return render(request,'includes/404-error-page.html', status=404)
 
def about_us(request):

    team_members = TeamMember.objects.all()
    return render(request, 'pages/about.html', {'team_members': team_members})

    return render(request, 'pages/about.html')
 
def security_tools(request):
    """
    View to display the Security Tools Arsenal page.
    """
    tools_data = [
        {
            'name': 'CyberArk PAM',
            'category': 'Identity Security',
            'icon_class': 'fas fa-shield-alt',  
            'description': 'Enterprise-grade privileged access management solution for securing critical credentials and preventing cyber attacks.',
            'key_benefits': [
                'Reduces privileged account vulnerabilities by 95%',
                'Automated credential rotation and discovery',
                'Real-time threat detection and response',
                'Compliance with major security frameworks',
            ],
            'features': ['Zero Trust Architecture', 'AI-Powered Analytics', 'Session Recording', 'Just-in-Time Access'],
            'service_url': '#'
        },
        {
            'name': 'Splunk SIEM',
            'category': 'Security Analytics',
            'icon_class': 'fas fa-chart-line', 
            'description': 'Advanced security information and event management platform for comprehensive threat detection and incident response.',
            'key_benefits': [
                'Faster threat detection and response times',
                'Centralized security monitoring across all systems',
                'Advanced analytics with machine learning',
                'Scalable cloud-native architecture',
            ],
            'features': ['Real-Time Monitoring', 'Machine Learning', 'Custom Dashboards', 'Automated Alerting'],
            'service_url': '#'
        },
        {
            'name': 'Nessus Scanner',
            'category': 'Vulnerability Management',
            'icon_class': 'fas fa-search', 
            'description': 'Industry-leading vulnerability assessment tool for identifying security weaknesses across your infrastructure.',
            'key_benefits': [
                'Comprehensive vulnerability coverage',
                'Accurate scanning with low false positives',
                'Regulatory compliance reporting',
                'Integration with existing security tools',
            ],
            'features': ['Network Scanning', 'Web App Testing', 'Configuration Auditing', 'Compliance Checks'],
            'service_url': '#'
        },
        {
            'name': 'Wireshark Analyzer',
            'category': 'Network Security',
            'icon_class': 'fas fa-wifi', 
            'description': 'Open-source network protocol analyzer for deep packet inspection and network troubleshooting.',
            'key_benefits': [
                'Deep network visibility and analysis',
                'Real-time packet capture and inspection',
                'Extensive protocol support',
                'Cost-effective open-source solution',
            ],
            'features': ['Packet Capture', 'Protocol Analysis', 'Traffic Filtering', 'Export Capabilities'],
            'service_url': '#'
        },
        {
            'name': 'Metasploit Framework',
            'category': 'Penetration Testing',
            'icon_class': 'fas fa-terminal',  
            'description': 'Comprehensive penetration testing platform for identifying and exploiting security vulnerabilities.',
            'key_benefits': [
                'Validate security defenses effectively',
                'Extensive exploit database and payloads',
                'Automated exploitation capabilities',
                'Professional reporting and documentation',
            ],
            'features': ['Exploit Database', 'Payload Generation', 'Post-Exploitation', 'Social Engineering'],
            'service_url': '/pen-testing'
        },
        {
            'name': 'Burp Suite Pro',
            'category': 'Web Application Security',
            'icon_class': 'fas fa-wrench', 
            'description': 'Leading web application security testing platform for finding and exploiting web vulnerabilities.',
            'key_benefits': [
                'Comprehensive web app security testing',
                'Advanced scanning and manual testing tools',
                'Extensible through custom plugins',
                'Industry-standard security testing platform',
            ],
            'features': ['Automated Scanning', 'Manual Testing Tools', 'Extensibility', 'Session Management'],
            'service_url': '/pen-testing'
        }
    ]

    context = {
        'title': 'Our Security Tools',
        'tools': tools_data
    }
    return render(request, 'pages/our_tools.html', context)



def what_we_do(request):
    return render(request, 'pages/what_we_do.html')

@login_required
def profile(request):
    # Ensure the user has a profile, create it if not
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=request.user)

    # Get student object if exists
    try:
        student = Student.objects.get(user=request.user)
        skill_count = Progress.objects.filter(student=student, completed=True).count()
    except Student.DoesNotExist:
        skill_count = 0

    achievement_count = UserChallenge.objects.filter(user=request.user, completed=True).count()

    # Fetch the list of completed challenges
    completed_challenges = UserChallenge.objects.filter(
        user=request.user, 
        completed=True
    ).select_related('challenge').order_by('-challenge__points')

    if request.method == 'POST':
        if 'save_photo' in request.POST:
            # Only handle avatar upload
            p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
            u_form = UserUpdateForm(instance=request.user)  # Don't update user fields
            if p_form.is_valid():
                # Only save the avatar field
                profile.avatar = p_form.cleaned_data['avatar']
                profile.save()
                messages.success(request, 'Your profile picture has been updated!')
            else:
                messages.error(request, 'Failed to update profile picture.')
            return redirect('profile')
        else:
            # Handle profile details update
            u_form = UserUpdateForm(request.POST, instance=request.user)
            p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
            if u_form.is_valid() and p_form.is_valid():
                u_form.save()
                # Save all fields except avatar
                profile.bio = p_form.cleaned_data['bio']
                profile.linkedin = p_form.cleaned_data['linkedin']
                profile.github = p_form.cleaned_data['github']
                profile.location = p_form.cleaned_data['location']
                profile.save()
                messages.success(request, 'Your profile has been updated successfully.')
            else:
                messages.error(request, 'Failed to update profile details.')
            return redirect('profile_details')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'profile': profile,
        'skill_count': skill_count,
        'achievement_count': achievement_count,
        'completed_challenges': completed_challenges,
    }

    return render(request, 'pages/profile.html', context)

@login_required
def profile_details(request):
    profile = request.user.profile
    return render(request, 'pages/profile_details.html', {
        'user': request.user,
        'profile': profile,
    })

def blog(request):
    return render(request, 'blog/index.html')
 
def appattack(request):
    return render(request, 'pages/appattack/main.html')

def skills_view(request):
    return render(request, 'pages/appattack/appattack_skills.html')



def form_success(request):
    return render(request, 'emails/form_success.html')

def policy_deployment(request):
    return render(request, 'pages/policy_deployment.html')
 
def appattack_join(request):

    if request.method == 'POST':
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        email = request.POST.get('email')
        message = request.POST.get('message')

        if not first_name or not last_name or not email or not message:
            messages.error(request, "All fields are required.")
            return render(request, 'pages/appattack/join.html')

        # Save the data
        ContactSubmission.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            message=message
        )

        # Prepare and send email
        try:
            subject = "Thank you for contacting us!"
            html_message = render_to_string('emails/contact_confirmation.html', {
                'first_name': first_name,
                'last_name': last_name,
                'message': message,
            })
            plain_message = strip_tags(html_message)

            send_mail(
                subject=subject,
                message=plain_message,
                from_email='hardhatcompanywebsite@gmail.com',
                recipient_list=[email],
                html_message=html_message,
                fail_silently=False,
            )
            messages.success(request, "Your message has been received, and a confirmation email has been sent.")
        except Exception as e:
            print(f"Email sending failed: {e}")
            messages.error(request, "Your message was received, but we couldn't send a confirmation email.")

        return redirect('form_success')


   # print("Hi");
    print(request.POST);

    return render(request, 'pages/appattack/join.html')


 
def products_services(request):
    return render(request, 'pages/malware_visualization/products_and_services.html')
 
def malwarehome(request):
    return render(request, 'pages/malware_visualization/main.html')

def malware_skills(request):
    return render(request, 'pages/malware_visualization/malware_skills.html')

 
def malware_joinus(request):
    return render(request, 'pages/malware_visualization/malware_viz_joinus.html')
 
def ptguihome(request):
    return render(request, 'pages/pt_gui/main.html')

def ptgui_skills(request):
    return render(request, 'pages/pt_gui/ptgui_skills.html')

 
def ptgui_contact_us(request):
    return render(request, 'pages/pt_gui/contact-us.html')
 
def faq(request):
    return render(request, 'pages/pt_gui/faq.html')
 
def ptgui_join_us(request):
    if request.method == 'POST':
        ddt_contact = DDT_contact(
            fullname = request.POST.get('fullname',''),
            email = request.POST.get('email',''),
            mobile = request.POST.get('mobile',''),
            message = request.POST.get('message',''),
        )
        ddt_contact.save()
        return redirect('ptgui_join_us')
    else:
        return render(request, 'pages/pt_gui/join_us.html')
 
def http_503(request):
    return render(request, 'pages/503.html')
 
def join_project(request):
    context = {'student_exists': False}
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save(commit=False)
            student.user = request.user
            student.save()
            form.save()
            print("Preferences saved successfully!")
            return redirect('/')
        else:
            print("Could not save preferences!")
    else:
        user = request.user
        if Student.objects.filter(user=user.id).exists():
            context['student_exists'] = True
        form = StudentForm()
 
    context['form'] = form
    return render(request, 'pages/joinproject.html', context)
 
def smishing_detection(request):
    return render(request, 'pages/smishing_detection/main.html')

def smishing_skills(request):
    return render(request, 'pages/smishing_detection/smishing_skills.html')

def achievements(request):
    """
    Visible to everyone.
    - Anonymous: all pills 'locked', progress 0%.
    - Authenticated: pill state & progress reflect that user's challenge activity.
      State rules per category:
        earned  = user has any completed challenge in that category
        started = user has any started challenge in that category (but none completed)
        locked  = otherwise
    Progress bar = (# earned pills) / (total categories) * 100
    """

    # 1) List every category that has at least one challenge
    base = (
        CyberChallenge.objects
        .values("category")
        .annotate(total=Count("id"))
        .order_by("category")
    )

    # 2) Build maps of started/completed counts for the current user (or empty if anon)
    started_map = {}
    completed_map = {}

    if request.user.is_authenticated:
        started_qs = (
            UserChallenge.objects
            .filter(user=request.user, started=True)
            .values("challenge__category")
            .annotate(n=Count("id"))
        )
        completed_qs = (
            UserChallenge.objects
            .filter(user=request.user, completed=True)
            .values("challenge__category")
            .annotate(n=Count("id"))
        )
        started_map   = {r["challenge__category"]: r["n"] for r in started_qs}
        completed_map = {r["challenge__category"]: r["n"] for r in completed_qs}

    # 3) Compose the pill list
    categories = []
    for row in base:
        raw   = row["category"]               # e.g., "Web_Security"
        total = row["total"]
        name  = raw.replace("_", " ")

        # Default: locked for anonymous
        if not request.user.is_authenticated:
            state = "locked"
        else:
            done   = completed_map.get(raw, 0)
            start  = started_map.get(raw, 0)
            state  = "earned" if done > 0 else ("started" if start > 0 else "locked")

        # Enable link only if started/earned
        url = reverse("category_challenges", args=[raw]) if state in ("started", "earned") else None

        categories.append({
            "raw": raw,
            "name": name,
            "total": total,
            "state": state,
            "url": url,
        })

    total_categories = len(categories)
    earned_categories = sum(1 for c in categories if c["state"] == "earned")
    percent = int((earned_categories / total_categories) * 100) if total_categories else 0

    return render(
        request,
        "pages/achievements.html",
        {
            "categories": categories,
            "percent": percent,
            "total_categories": total_categories,
            "earned_categories": earned_categories,
        },
    )

from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q  # keep using Count, etc.
from .models import CyberChallenge, UserChallenge

def category_challenges(request, category):
    challenges = CyberChallenge.objects.filter(category=category).order_by("id")

    if request.user.is_authenticated:
        for ch in challenges:
            uc, _ = UserChallenge.objects.get_or_create(user=request.user, challenge=ch)
            if not uc.started:
                uc.started = True
                uc.save()

    return render(request, "pages/challenges/category_challenges.html", {
        "category": category,
        "challenges": challenges
    })

# views.py
from django.shortcuts import render
from django.db.models import Count, Q
# import your models
from .models import CyberChallenge, UserChallenge

def achievements(request):
    """
    Build per-category pill status without needing a 'started' field.
    - Locked: user has no attempts in the category
    - Started: user has at least 1 attempt in the category (not necessarily completed)
    - Earned: user has at least 1 completed challenge in the category
    """
    # All categories + how many total challenges in each
    categories_qs = (
        CyberChallenge.objects
        .values("category")
        .annotate(total=Count("id"))
        .order_by("category")
    )

    total_challenges = sum(row["total"] for row in categories_qs)

    # Defaults for anonymous users
    started_cats = set()
    earned_cats = set()
    total_completed = 0

    if request.user.is_authenticated:
        # Aggregate attempts for this user by category
        user_rows = (
            UserChallenge.objects
            .filter(user=request.user)
            .values("challenge__category")
            .annotate(
                num_attempts=Count("id"),
                num_completed=Count("id", filter=Q(completed=True)),
            )
        )

        # Derive sets for quick membership checks
        started_cats = {r["challenge__category"] for r in user_rows if r["num_attempts"] > 0}
        earned_cats  = {r["challenge__category"] for r in user_rows if r["num_completed"] > 0}

        # Overall completed count across all categories
        total_completed = sum(r["num_completed"] for r in user_rows)

    # Build pill objects for template
    categories = []
    for row in categories_qs:
        raw = row["category"]                 # e.g., "Web_Security"
        pretty = raw.replace("_", " ")
        if raw in earned_cats:
            status = "earned"
        elif raw in started_cats:
            status = "started"
        else:
            status = "locked"

        categories.append({
            "raw": raw,        # slug used for links
            "name": pretty,    # label
            "total": row["total"],
            "status": status,  # locked | started | earned
        })

    percent = round((total_completed / total_challenges) * 100) if total_challenges else 0

    return render(request, "pages/achievements.html", {
        "percent": percent,
        "categories": categories,
        "total_completed": total_completed,
        "total_challenges": total_challenges,
    })




 
def smishingdetection_join_us(request):
 
    if request.method == 'POST':
        form = sd_JoinUsForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your message has been successfully sent")
            return redirect('smishingdetection_join_us')  # Redirect to the same page after form submission
        else:
            messages.error(request, "Please fill the form correctly")
    else:
        form = sd_JoinUsForm()
    return render(request, 'pages/smishing_detection/join_us.html', {'form': form})
 
# Upskill Pages
def upskill_repository(request):
    return render(request), 'pages/upskilling/repository.html'
 
def upskill_roadmap(request):
    return render(request), 'pages/upskilling/roadmap.html'
 
def upskill_progress(request):
    return render(request), 'pages/upskilling/progress.html'

def UpskillSuccessView(request):
    return render(request, 'pages/upskilling/UpskillingFormSuccess.html')
def UpskillingJoinProjectView(request):
    student_exists = Student.objects.filter(user=request.user).exists()

    if student_exists:
        return render(request, 'joinproject.html', {'student_exists': True})

    if request.method == 'POST':
        form = Upskilling_JoinProjectForm(request.POST)
        if form.is_valid():
            student = form.save(commit=False)
            student.user = request.user  # Assign the current user
            student.save()
            return redirect('success_page')  # Redirect to success page
    else:
        form = Upskilling_JoinProjectForm()

    return render(request, 'joinproject.html', {'form': form, 'student_exists': False})

# OTP-Based Login
def login_with_otp(request):
    """
    For Login
    """
    if request.method == 'POST':
        # First, verify reCAPTCHA
        token = request.POST.get('g-recaptcha-response')
        secret_key = settings.RECAPTCHA_SECRET_KEY

        recaptcha_response = requests.post(
            'https://www.google.com/recaptcha/api/siteverify',
            data={'secret': secret_key, 'response': token}
        )

        result = recaptcha_response.json()

        if settings.DEBUG:
            print("DEBUG MODE: reCAPTCHA result:", result)

        if not result.get('success') or result.get('score', 0) < 0.5:
            messages.error(request, "reCAPTCHA verification failed. Please try again.")
            if settings.DEBUG:
                print("DEBUG MODE: reCAPTCHA failed with response:", result)
            return render(request, 'accounts/sign-in.html')

        # reCAPTCHA passed — continue login logic
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user:
            otp = random.randint(100000, 999999)
            request.session['otp'] = otp
            request.session['user_id'] = user.id
            request.session['otp_timestamp'] = time.time()  #Set time
            request.session['otp_attempts'] = 0  # Reset attempts on new OTP

            send_mail(
                subject="Your OTP Code",
                message=f"Your OTP code is {otp}, it expires in 5 minutes. Use it to verify your login.",
                from_email="deakinhardhatwebsite@gmail.com",
                recipient_list=[user.email],
                fail_silently=False,
            )

            if settings.DEBUG:
                print(f"DEBUG MODE: OTP for {user.email} is {otp}")

            messages.success(request, "An OTP has been sent to your email. Please enter it below to continue.")
            return redirect('verify_otp')
        else:
            messages.error(request, "Invalid username or password.")

            if settings.DEBUG:
                print(f"DEBUG MODE: Invalid login attempt for username: {username}")
                print(f"DEBUG MODE: Password entered: {password}")

    return render(request, 'accounts/sign-in.html')



# Verify OTP
def verify_otp(request):
    """
    OTP verification during login.
    Locks out after 5 failed attempts or 5 minutes by redirecting to login.
    """
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        saved_otp = request.session.get('otp')
        user_id = request.session.get('user_id')

        # Initialize OTP timestamp if not already set
        otp_timestamp = request.session.get('otp_timestamp')
        if not otp_timestamp:
            request.session['otp_timestamp'] = time.time()
        else:
            elapsed = time.time() - otp_timestamp
            if elapsed > 300:  # 300 seconds = 5 minutes
                messages.error(request, "OTP session expired. Please log in again.")
                print("[DEBUG] OTP expired after 5 minutes. Elapsed time: {:.2f} seconds".format(elapsed))
                request.session.flush()
                return redirect('login')

        if entered_otp and saved_otp and int(entered_otp) == int(saved_otp):
            User = get_user_model()
            try:
                user = User.objects.get(id=user_id)
                login(request, user)
                # Clear session data on success
                request.session.pop('otp', None)
                request.session.pop('user_id', None)
                request.session.pop('otp_attempts', None)
                request.session.pop('otp_timestamp', None)
                messages.success(request, "Login successful!")
                return redirect(get_login_redirect_url(user))
            except User.DoesNotExist:
                messages.error(request, "User does not exist.")
        else:
            # Handle OTP failure
            otp_attempts = request.session.get('otp_attempts', 0) + 1
            request.session['otp_attempts'] = otp_attempts
            print(f"[DEBUG] Failed OTP attempt #{otp_attempts} for user ID: {user_id}")

            if otp_attempts >= 5:
                messages.error(request, "Too many failed attempts. Redirecting to login.")
                print("[DEBUG] Too many failed attempts. Redirecting to login.")
                request.session.flush()
                return redirect('login')

            messages.error(request, f"Invalid OTP. Attempt {otp_attempts}/5.")

    return render(request, 'accounts/verify-otp.html')

# Search Suggestions
def SearchSuggestions(request):
    query = request.GET.get('query', '')
    if len(query) >= 2:
        suggestions = User.objects.filter(name__icontains=query).values_list('name', flat=True)[:5]
        return JsonResponse(list(suggestions), safe=False)
    return JsonResponse([], safe=False)

#Search-Results page

# --- normalize function ---
def normalize(word):
    return re.sub(r'[^a-z0-9]', '', word.lower()) if word else ''  

# --- get_suggestions function ---
def get_suggestions(query):
    if not query:
        return []

    normalized_query = normalize(query)

    User = get_user_model()

    # Build dictionary from database
    raw_dictionary = list(Project.objects.values_list("title", flat=True)) + \
        list(Course.objects.values_list("title", flat=True)) + \
        list(Article.objects.values_list("title", flat=True)) + \
        list(Skill.objects.values_list("name", flat=True)) + \
        list(User.objects.values_list("first_name", flat=True)) + \
        list(User.objects.values_list("last_name", flat=True)) + \
        list(BlogPost.objects.values_list("title", flat=True))

    # Create mapping {normalized → original}
    dictionary_map = {normalize(w): w for w in raw_dictionary if w}
    dictionary = list(dictionary_map.keys())

    # Find close matches
    matches = difflib.get_close_matches(normalized_query, dictionary, n=5, cutoff=0.5)

    # Map back to original words
    return [dictionary_map[m] for m in matches if m != normalized_query]

# --- Main SearchResults function ---
def SearchResults(request):
    User = get_user_model()
    query = request.GET.get('q') or request.POST.get('q', '')  # GET support and strip
    query = query.strip()  

    sort = request.GET.get('sort', '')          # newest / oldest  
    start_date = request.GET.get('start_date')  # from filter form  
    end_date = request.GET.get('end_date')      
    content_type = request.GET.getlist('type')  # multiple checkboxes possible  

    # function is defined before we call it
    suggestion = get_suggestions(query)  
    
    if not query:
        return render(request, 'pages/search-results.html', {
            'searched': '',
            'suggestion': '',
            'webpages': [],
            'projects': [],
            'courses': [],
            'skills': [],
            'articles': [],
            'users': [],
            'students': [],
            'contacts': []
    })

    # --- Projects ---
    project_results = Project.objects.filter(title__icontains=query)

    # --- Courses ---
    course_results = Course.objects.filter(title__icontains=query) | Course.objects.filter(code__icontains=query)

    # --- Articles ---
    article_results = Article.objects.filter(title__icontains=query)
    if start_date:  
        article_results = article_results.filter(date__gte=parse_date(start_date))  
    if end_date:  
        article_results = article_results.filter(date__lte=parse_date(end_date))  

    # --- Users ---
    users = User.objects.filter(
        first_name__icontains=query
    ) | User.objects.filter(
        last_name__icontains=query
    ) | User.objects.filter(
        email__icontains=query
    )

    # --- Apply sorting ---
    if sort == "newest":  
        article_results = article_results.order_by('-date')  
    elif sort == "oldest":  
        article_results = article_results.order_by('date')  

    # --- Type filter ---
    if content_type:  
        if "projects" not in content_type:
            project_results = Project.objects.none()  
        if "articles" not in content_type:
            article_results = Article.objects.none()  
        if "users" not in content_type:
            users = User.objects.none()  
        if "courses" not in content_type:
            course_results = Course.objects.none()  
        if "skills" not in content_type:
            skills = Skill.objects.none()  
        if "students" not in content_type:
            students = Student.objects.none()  
        if "contacts" not in content_type:
            contacts = Contact.objects.none()  
        if "webpages" not in content_type:
            webpages = Webpage.objects.none()  
    else:
        # show everything
        students = Student.objects.filter(user__first_name__icontains=query) | \
           Student.objects.filter(user__last_name__icontains=query) | \
           Student.objects.filter(user__email__icontains=query)  
        contacts = Contact.objects.filter(name__icontains=query)  
        webpages = Webpage.objects.filter(title__icontains=query)

    # --- Compile results ---
    results = {
        'searched': query,
        'suggestion': suggestion,
        'webpages': Webpage.objects.filter(title__icontains=query),
        'projects': project_results,
        'users': users,
        'courses': course_results,
        'skills': Skill.objects.filter(name__icontains=query),
        'articles': Article.objects.filter(title__icontains=query),
        'students': students,  
        'contacts': contacts,
    }
    return render(request, 'pages/search-results.html', results)
   
#    if request.method == 'GET':
#        searched = request.GET.get('searched')
#        results = None
#        if searched:
#            results = Webpage.objects.filter(url__icontains=searched)
#        return render(request, 'pages/search-results.html', {})
 
#
   
##def dynamic_articles_view(request):
##    context['object_list'] = article.objects.filter(title__icontains=request.GET.get('search'))
##    return render(request, "encyclopedia/article_detail.html", context)


def Deakin_Threat_mirror_main(request):
    return render(request, 'pages/DeakinThreatmirror/main.html')

def deakinthreatmirror_skills(request):
    return render(request, 'pages/DeakinThreatmirror/deakinthreatmirror_skills.html')



def Vr_main(request):
    return render(request, 'pages/Vr/main.html')

def cybersafe_vr_skills(request):
    return render(request, 'pages/Vr/cybersafe_vr_skills.html')


# Authentication

def client_login(request):
    form = ClientLoginForm
    return render(request, 'accounts/sign-in-client.html',{'form': form})
    
## Web-Form 

def website_form(request):
    if request.method == "POST":
        form = NewWebURL(request.POST)
        if form.is_valid():
            t = form.cleaned_data["title"]
            u = form.cleaned_data["url"]
            w = Webpage(title=t, url=u)
            w.save()
        return render(request, 'pages/website-form.html', {"form":form})
    else:
        form = NewWebURL()
        return render(request, 'pages/website-form.html', {"form":form})

        
    
 
 
# Authentication
 
class UserLoginView(LoginView):
    template_name = 'accounts/sign-in.html'
    form_class = UserLoginForm
    
    def form_valid(self, form):
        # Force new session to rotate session key (prevents fixation)
        self.request.session.flush()  # <-- This destroys old session
        
        # Successful login, proceed as normal
        response = super().form_valid(form)

        # Store session info for hijack protection
        request = self.request
        request.session['ip_address'] = self.get_client_ip(request)
        request.session['user_agent'] = request.META.get('HTTP_USER_AGENT', '')
        request.session['session_token'] = request.session.session_key

        return response

    def get_success_url(self):
        """Override to implement conditional redirect based on join-us completion"""
        user = self.request.user
        return get_login_redirect_url(user)

    def form_invalid(self, form):
        # Increment the failed login attempts
        failed_attempts = cache.get('failed_login_attempts', 0) + 1
        cache.set('failed_login_attempts', failed_attempts, timeout=60)  # Store for 1 minute

        # Check if the limit is exceeded
        if failed_attempts >= 5:  # Set your limit here
            # Set the global lockout
            cache.set('global_lockout', True, timeout=60)  # Lockout for 1 minute
            # Set the lockout start time
            cache.set('lockout_start_time', timezone.now(), timeout=60)  # Lockout for 1 minute
            return redirect(reverse('rate_limit_exceeded'))  # Redirect to a rate limit exceeded page

        return super().form_invalid(form)

    def get_client_ip(self, request):
        # Using x_forwarded_for allows for proxy bypass to give the true IP of a user
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR')

class AdminLoginView(LoginView):
    """Specialised login view for admin users via /accounts/admin"""
    template_name = 'accounts/sign-in.html'
    form_class = UserLoginForm

    def form_valid(self, form):
        user = form.get_user()

        # Check if user has admin privileges (staff or superuser - treated the same)
        if not user.is_admin_user():
            messages.error(self.request, 'Access denied. Admin privileges required.')
            return redirect('login')

        # Force new session to rotate session key (prevents fixation)
        self.request.session.flush()

        # Successful login, proceed as normal
        response = super().form_valid(form)

        # Enhanced admin session tracking
        request = self.request
        client_ip = self.get_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')

        # Store regular session info for hijack protection
        request.session['ip_address'] = client_ip
        request.session['user_agent'] = user_agent
        request.session['session_token'] = request.session.session_key

        # Mark this as an admin session
        request.session['is_admin_session'] = True
        request.session['admin_login_time'] = timezone.now().isoformat()

        # Create AdminSession record for tracking
        from .models import AdminSession

        # End any existing active admin sessions for this user
        AdminSession.objects.filter(user=user, is_active=True).update(
            is_active=False, 
            logout_time=timezone.now(),
            logout_reason='new_session'
        )

        # Create new admin session record
        admin_session = AdminSession.objects.create(
            user=user,
            session_key=request.session.session_key,
            ip_address=client_ip,
            user_agent=user_agent
        )

        # Store admin session ID in session for tracking
        request.session['admin_session_id'] = admin_session.id

        # Log admin login
        import logging
        logger = logging.getLogger('audit_logger')
        logger.info(f"Admin login: {user.email} from IP {client_ip}")

        messages.success(request, f'Welcome back, {user.get_full_name()}! Admin session started.')

        return response

    def get_client_ip(self, request):
        # Using x_forwarded_for allows for proxy bypass to give the true IP of a user
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR')


def rate_limit_exceeded(request):
    remaining_time = 60  # Use the helper function

    return render(request, 'accounts/rate_limit_exceeded.html', {
        'message': 'Too many login attempts. Please try again later.',
        'wait_time': remaining_time,
    })
 
def logout_view(request):
    logout(request)
    return redirect('/')
 
def password_gen(request):
    return JsonResponse({'data': gen_password()}, status=200)
 

@csrf_exempt
def VerifyOTP(request):
    """
    For account verification via OTP.
    """
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        saved_otp = request.session.get('otp')
        user_id = request.session.get('user_id')

        if entered_otp and saved_otp and int(entered_otp) == int(saved_otp):
            User = get_user_model()  # Fetch the custom User model
            try:
                user = User.objects.get(id=user_id)
                user.is_verified = True  # Mark the user as verified
                user.is_active = True   # Ensure the account is active
                user.save()             # Save changes

                # Clear session data
                request.session.pop('otp', None)
                request.session.pop('user_id', None)

                # Generate and store passkeys (5 passkeys)
                passkeys = []
                for _ in range(5):
                    new_key = Passkey.generate_passkey()
                    Passkey.objects.create(user=user, key=new_key)
                    passkeys.append(new_key)

                # Send email with passkeys
                send_mail(
                    subject="Your Lifetime Passkeys for HardHat Login",
                    message=(
                        f"Hello {user.first_name},\n\n"
                        "Your email has been successfully verified! 🎉\n\n"
                        "Here are your lifetime passkeys:\n\n"
                        f"{chr(10).join(passkeys)}\n\n"
                        "You can use these passkeys instead of OTP during login.\n\n"
                        "🔹 Keep them safe, as they are your permanent authentication keys.\n"
                        "🔹 If you ever need new passkeys, contact support.\n\n"
                        "Regards,\nHardHat Enterprises"
                    ),
                    from_email="deakinhardhatwebsite@gmail.com",
                    recipient_list=[user.email],
                    fail_silently=False,
                )

                print(f"OTP matched. Account for {user.email} has been activated and verified.")
                print(f"Passkeys sent to {user.email}: {passkeys}") 

                messages.success(request, "Your account has been successfully verified! Your passkeys have been sent via email.")
                return redirect('/')

            except User.DoesNotExist:
                messages.error(request, "User does not exist. Please register again.")
                return redirect('/accounts/signup/')
        else:
            messages.error(request, "Invalid OTP. Please try again.")

    return render(request, 'accounts/verify_token.html')

def login_with_passkey(request):
    """
    Login using passkey instead of OTP, then redirect to CAPTCHA verification.
    """
    if request.method == "POST":
        email = request.POST.get("email")
        passkey = request.POST.get("passkey")

        try:
            user = get_user_model().objects.get(email=email)

            if Passkey.objects.filter(user=user, key=passkey).exists():
                request.session['pending_user_id'] = user.id  # Store user ID temporarily
                login(request, user)

                # Save IP and browser info when logging in with passkey
                user.last_login_ip = get_client_ip(request)
                user.last_login_browser = request.META.get('HTTP_USER_AGENT', '')[:256]
                print("Tracked login IP:", user.last_login_ip)
                print("Tracked browser:", user.last_login_browser)
                user.save(update_fields=['last_login_ip', 'last_login_browser'])

                messages.success(request, "Passkey verified! Please complete CAPTCHA verification.")
                request.session['is_otp_verified'] = True  # Mark OTP as verified
                return redirect(get_login_redirect_url(user))
            else:
                messages.error(request, "Invalid passkey. Please try again.")
        except get_user_model().DoesNotExist:
            messages.error(request, "No user found with this email.")

    return render(request, "accounts/passkey_login.html")


def reset_passkeys_request(request):
    if request.method == "POST":
        email = request.POST.get("email")
        last_name = request.POST.get("last_name")
        password = request.POST.get("password")

        try:
            user = User.objects.get(email=email, last_name=last_name)
        except User.DoesNotExist:
            messages.error(request, "Invalid details. Please try again.")
            return redirect("reset_passkeys_request")

        authenticated_user = authenticate(email=email, password=password)
        if authenticated_user is None:
            messages.error(request, "Incorrect password.")
            return redirect("reset_passkeys_request")

        # Generate and send OTP
        otp = random.randint(100000, 999999)
        request.session["reset_passkeys_otp"] = otp
        request.session["reset_passkeys_user_id"] = user.id

        send_mail(
            subject="Reset Your Passkeys - HardHat",
            message=f"Your OTP for resetting passkeys is: {otp}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )

        messages.success(request, "OTP sent to your email.")
        return redirect("reset_passkeys_verify")

    return render(request, "accounts/reset_passkeys_request.html")

def reset_passkeys_verify(request):
    if request.method == "POST":
        entered_otp = request.POST.get("otp")
        saved_otp = request.session.get("reset_passkeys_otp")
        user_id = request.session.get("reset_passkeys_user_id")

        if not (entered_otp and saved_otp and user_id):
            messages.error(request, "Session expired. Please try again.")
            return redirect("reset_passkeys_request")

        if int(entered_otp) != int(saved_otp):
            messages.error(request, "Invalid OTP. Please try again.")
            return redirect("reset_passkeys_verify")

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            messages.error(request, "User not found.")
            return redirect("reset_passkeys_request")

        # Remove old passkeys
        Passkey.objects.filter(user=user).delete()

        # Generate 5 new passkeys
        new_passkeys = ["".join(random.choices(string.ascii_letters + string.digits, k=12)) for _ in range(5)]
        for key in new_passkeys:
            Passkey.objects.create(user=user, key=key)

        # Send new passkeys via email
        send_mail(
            subject="Your New Passkeys - HardHat",
            message=(
                f"Hello {user.first_name},\n\n"
                "Your passkeys have been successfully reset! 🔄\n\n"
                "Here are your new lifetime passkeys:\n\n"
                f"{chr(10).join(new_passkeys)}\n\n"
                "You can use these passkeys instead of OTP during login.\n\n"
                "🔹 Keep them safe, as they are your permanent authentication keys.\n"
                "🔹 If you ever need to reset them again, you can do so from the login page.\n\n"
                "If you did not request this reset, please contact support immediately.\n\n"
                "Regards,\nHardHat Enterprises"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )


        # Clear session data
        del request.session["reset_passkeys_otp"]
        del request.session["reset_passkeys_user_id"]

        messages.success(request, "Your passkeys have been reset and emailed to you.")
        return redirect("passkey_login")

    return render(request, "accounts/reset_passkeys_verify.html")

def register_client(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        business_name = request.POST.get('business_name')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        form = ClientRegistrationForm(request.POST)
       
        if form.is_valid():
            form.save()
            
            return redirect("package_plan")
            # return redirect("verify-email", username=request.POST['first_name'])
        else:
            print("Registration failed!")
    else:
        form = ClientRegistrationForm()
 
    context = { 'form': form }
    return render(request, 'accounts/sign-up-client.html', context)

logger = logging.getLogger(__name__)  # Initialize logger

def register(request):
    """
    Handles user registration and OTP verification.
    """
    if request.method == 'POST':
        post_data = request.POST.copy()  # Copy POST data
        post_data['password1'] = "HIDDEN FOR SAFETY"  # Hide passwords
        post_data['password2'] = "HIDDEN FOR SAFETY"
        
        logger.info(f"POST Data (Sanitized): {post_data}")  # Log without passwords

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')

        print(f"Received Registration Request: First Name: {first_name}, Last Name: {last_name}, Email: {email}, Password: HIDDEN FOR SAFETY")

        form = RegistrationForm(request.POST)

        if form.is_valid():
            try:
                user = form.save(commit=False)  # Save user instance without committing
                user.set_password(form.cleaned_data['password1'])  # Hash the password
                user.save()  # Save the user to the database
                print("User saved to database.")  # Success log

                # Generate OTP and send email
                otp = random.randint(100000, 999999)
                email = form.cleaned_data.get('email')
                send_mail(
                    subject="User Data",
                    message=(
                        f"Hello from HardHat Enterprise! Verify Your Mail with the OTP: \n{otp}\n"
                        "If you didn't request an OTP or open an account with us, please contact us at your earliest convenience.\n\n"
                        "Regards, \nHardhat Enterprises"
                    ),
                    from_email="deakinhardhatwebsite@gmail.com",
                    recipient_list=[user.email],
                    fail_silently=False,
                )

                request.session['otp'] = otp
                request.session['user_id'] = user.id

                # Print OTP to terminal if DEBUG is True
                if settings.DEBUG:
                    print(f"DEBUG MODE: OTP for {user.email} is {otp}")

                # Redirect to verify token page with context
                messages.success(request, "Account created successfully! Check your email for the OTP.")
                return redirect('verifyEmail')
                
            except Exception as e:
                logger.error(f"Error saving user or sending email: {e}")
                messages.error(request, "An error occurred while creating the account. Please try again.")
        else:
            logger.error(f"Form is invalid. Errors: {form.errors}")
            messages.error(request, "Please fix the errors below.")
    else:
        form = RegistrationForm()

    return render(request, 'accounts/sign-up.html', {'form': form})


User = get_user_model()

def post_otp_login_captcha(request):
    """
    Handles CAPTCHA verification after OTP verification before logging in the user.
    """
    user_id = request.session.get('user_id')
    is_otp_verified = request.session.get('is_otp_verified', False)  # Ensure OTP was verified first

    if not is_otp_verified or not user_id:
        messages.error(request, "OTP verification required before CAPTCHA.")
        return redirect('login_with_otp')

    if request.method == 'POST':
        form = CaptchaForm(request.POST)
        if form.is_valid():
            try:
                user = User.objects.get(id=user_id)  # Get the user based on session ID
                login(request, user)  # Log in the user after CAPTCHA verification
                del request.session['otp']
                del request.session['user_id']
                del request.session['is_otp_verified']  # Clean up session data
                messages.success(request, "Login successful!")
                return redirect(get_login_redirect_url(user))  # Conditional redirect based on join-us completion
            except User.DoesNotExist:
                messages.error(request, "User not found. Please log in again.")
                return redirect('login_with_otp')
        else:
            messages.error(request, "CAPTCHA verification failed. Please try again.")
    else:
        form = CaptchaForm()

    return render(request, 'accounts/post_otp_captcha.html', {'form': form})

def get_client_ip(request):
    # Using x_forwarded_for allows for proxy bypass to give the true IP of a user
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')


@require_POST
@csrf_protect
def microsoft_login(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        access_token = data.get('access_token')
        if not access_token:
            return JsonResponse({'error': 'Missing access token'}, status=400)

        # Verify token with Microsoft Graph API
        graph_url = 'https://graph.microsoft.com/v1.0/me'
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        
        response = requests.get(graph_url, headers=headers)
        if response.status_code != 200:
            return JsonResponse({'error': 'Invalid access token'}, status=401)

        user_info = response.json()
        user_email = user_info.get('mail') or user_info.get('userPrincipalName')
        if not user_email:
            return JsonResponse({'error': 'Email not present in token'}, status=400)

        # Validate that the user is from Deakin University
        if not user_email.endswith('@deakin.edu.au'):
            return JsonResponse({
                'error': 'Access restricted to Deakin University students and staff. Please use a @deakin.edu.au email address.'
            }, status=403)

        first_name = user_info.get('givenName', '')
        last_name = user_info.get('surname', '')
        display_name = user_info.get('displayName', f'{first_name} {last_name}'.strip())
        
        # Extract additional Deakin-specific information
        job_title = user_info.get('jobTitle', '')
        department = user_info.get('department', '')
        office_location = user_info.get('officeLocation', '')

        UserModel = get_user_model()
        user, created = UserModel.objects.get_or_create(
            email=user_email,
            defaults={
                'first_name': first_name,
                'last_name': last_name,
                'username': user_email.split('@')[0],  # Use email prefix as username
                'is_active': True,
                'is_verified': True,
                'is_staff': job_title and ('staff' in job_title.lower() or 'lecturer' in job_title.lower() or 'professor' in job_title.lower()),
            }
        )

        if created:
            # Set an unusable password for social-only accounts
            user.set_unusable_password()
            user.save()
            
            # Log successful Deakin user registration
            if settings.DEBUG:
                print(f'New Deakin user registered: {user_email} - {display_name}')
        else:
            # Update existing user information
            user.first_name = first_name
            user.last_name = last_name
            user.is_verified = True
            user.save(update_fields=['first_name', 'last_name', 'is_verified'])

        login(request, user)

        # Track login metadata
        try:
            user.last_login_ip = get_client_ip(request)
            user.last_login_browser = request.META.get('HTTP_USER_AGENT', '')[:256]
            user.save(update_fields=['last_login_ip', 'last_login_browser'])
        except Exception:
            pass

        # Log successful Deakin authentication
        if settings.DEBUG:
            print(f'Deakin user authenticated: {user_email} - {display_name}')

        # Redirect to dashboard for Microsoft OAuth users
        redirect_url = '/dashboard/'
        
        return JsonResponse({'redirect_url': redirect_url})

    except ValueError:
        return JsonResponse({'error': 'Invalid request body'}, status=400)
    except Exception as e:
        if settings.DEBUG:
            print('Microsoft login error:', str(e))
        return JsonResponse({'error': 'Authentication failed'}, status=401)


def microsoft_callback(request):
    """
    AGGRESSIVE Microsoft OAuth callback - NEVER redirects to login page
    """
    from django.http import HttpResponseRedirect
    
    try:
        # Get the authorization code from the callback
        code = request.GET.get('code')
        error = request.GET.get('error')
        
        if error:
            print(f"DEBUG: Microsoft authentication error: {error} - redirecting to dashboard anyway")
            return HttpResponseRedirect('/dashboard/')
        
        if not code:
            print(f"DEBUG: No authorization code - redirecting to dashboard anyway")
            return HttpResponseRedirect('/dashboard/')
        
        # Redirect to dashboard for successful authentication
        messages.success(request, 'Microsoft authentication successful! Welcome to your dashboard.')
        return HttpResponseRedirect('/dashboard/')
        
    except Exception as e:
        if settings.DEBUG:
            print('Microsoft callback error:', str(e))
        print(f"DEBUG: Exception occurred - redirecting to dashboard anyway")
        # NEVER redirect to login - always dashboard
        return HttpResponseRedirect('/dashboard/')


def microsoft_oauth_login(request):
    """
    MINIMAL Microsoft OAuth login - just redirect to Microsoft
    """
    from urllib.parse import urlencode
    from django.http import HttpResponseRedirect, HttpResponse
    
    print(f"DEBUG: MINIMAL Microsoft OAuth login called")
    
    # TEMPORARY: Test if OAuth login is being called
    if request.GET.get('test') == 'true':
        return HttpResponse("OAUTH LOGIN REACHED! This means the URL routing is working.")
    
    # Set a simple flag that we're doing OAuth
    request.session['doing_oauth'] = True
    request.session['oauth_redirect_to'] = '/dashboard/'
    
    # Use the same redirect URI that's configured in Azure AD
    redirect_uri = 'http://localhost:8000/complete/azuread-tenant-oauth2/'
    print(f"DEBUG: Using redirect URI: {redirect_uri}")
    
    # Microsoft OAuth authorization URL
    auth_url = 'https://login.microsoftonline.com/common/oauth2/v2.0/authorize'
    
    params = {
        'client_id': settings.SOCIAL_AUTH_AZUREAD_TENANT_OAUTH2_KEY,
        'response_type': 'code',
        'redirect_uri': redirect_uri,
        'scope': 'openid email profile',
        'response_mode': 'query',
        'prompt': 'login',  # Force fresh login
    }
    
    auth_url_with_params = f"{auth_url}?{urlencode(params)}"
    
    print(f"DEBUG: Redirecting to Microsoft OAuth: {auth_url_with_params}")
    
    return HttpResponseRedirect(auth_url_with_params)


def microsoft_oauth_callback(request):
    """
    AGGRESSIVE OAuth callback - NEVER redirects to login page
    """
    from django.contrib.auth import login
    from django.contrib.auth.models import User
    from django.http import HttpResponseRedirect, HttpResponse
    import requests
    
    print(f"DEBUG: ===== MICROSOFT OAUTH CALLBACK STARTED =====")
    print(f"DEBUG: Request path: {request.path}")
    print(f"DEBUG: Request method: {request.method}")
    print(f"DEBUG: Request GET params: {request.GET}")
    print(f"DEBUG: Session keys before: {list(request.session.keys())}")
    print(f"DEBUG: User authenticated before: {request.user.is_authenticated}")
    
    # TEMPORARY: Just show a simple message to test if callback is reached
    if request.GET.get('test') == 'true':
        return HttpResponse("OAUTH CALLBACK REACHED! This means the URL routing is working.")
    
    # ALWAYS redirect to dashboard - no exceptions
    try:
        # Get the authorization code from the callback
        code = request.GET.get('code')
        
        print(f"DEBUG: OAuth callback - code: {code[:20] if code else 'None'}...")
        
        if not code:
            print("DEBUG: No authorization code - redirecting to dashboard anyway")
            return HttpResponseRedirect('/dashboard/')
        
        # Exchange code for access token
        token_url = 'https://login.microsoftonline.com/common/oauth2/v2.0/token'
        token_data = {
            'client_id': settings.SOCIAL_AUTH_AZUREAD_TENANT_OAUTH2_KEY,
            'client_secret': settings.SOCIAL_AUTH_AZUREAD_TENANT_OAUTH2_SECRET,
            'code': code,
            'grant_type': 'authorization_code',
            'redirect_uri': 'http://localhost:8000/complete/azuread-tenant-oauth2/',
        }
        
        print(f"DEBUG: Requesting access token...")
        token_response = requests.post(token_url, data=token_data)
        
        if token_response.status_code != 200:
            print(f"DEBUG: Token request failed - redirecting to dashboard anyway")
            return HttpResponseRedirect('/dashboard/')
        
        token_json = token_response.json()
        access_token = token_json.get('access_token')
        
        if not access_token:
            print("DEBUG: No access token - redirecting to dashboard anyway")
            return HttpResponseRedirect('/dashboard/')
        
        # Get user info from Microsoft Graph
        user_info_url = 'https://graph.microsoft.com/v1.0/me'
        headers = {'Authorization': f'Bearer {access_token}'}
        
        print(f"DEBUG: Requesting user info...")
        user_response = requests.get(user_info_url, headers=headers)
        
        if user_response.status_code != 200:
            print(f"DEBUG: User info request failed - redirecting to dashboard anyway")
            return HttpResponseRedirect('/dashboard/')
        
        user_json = user_response.json()
        email = user_json.get('mail') or user_json.get('userPrincipalName')
        
        print(f"DEBUG: Microsoft user info - email: {email}")
        
        if not email:
            print("DEBUG: No email address - redirecting to dashboard anyway")
            return HttpResponseRedirect('/dashboard/')
        
        # Check if it's a Deakin email - but still redirect to dashboard
        if not email.endswith('@deakin.edu.au'):
            print(f"DEBUG: Non-Deakin email {email} - redirecting to dashboard anyway")
            return HttpResponseRedirect('/dashboard/')
        
        # Get or create user - use the correct User model
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        try:
            user = User.objects.get(email=email)
            print(f"DEBUG: Found existing user: {user.email}")
        except User.DoesNotExist:
            user = User.objects.create_user(
                username=email,
                email=email,
                first_name=user_json.get('givenName', ''),
                last_name=user_json.get('surname', ''),
                is_active=True,
            )
            print(f"DEBUG: Created new user: {user.email}")
        
        # Ensure user is active
        if not user.is_active:
            user.is_active = True
            user.save()
            print(f"DEBUG: Activated user: {user.email}")
        
        # Log the user in
        print(f"DEBUG: About to log in user: {user.email}")
        print(f"DEBUG: User ID: {user.id}")
        print(f"DEBUG: User is_active: {user.is_active}")
        print(f"DEBUG: User backend: {user.backend if hasattr(user, 'backend') else 'No backend'}")
        
        # Ensure user has a backend for authentication
        if not hasattr(user, 'backend'):
            user.backend = 'django.contrib.auth.backends.ModelBackend'
        
        # Force login with explicit backend
        from django.contrib.auth import login
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        
        print(f"DEBUG: After login - User authenticated: {request.user.is_authenticated}")
        print(f"DEBUG: After login - User email: {request.user.email}")
        print(f"DEBUG: After login - User ID: {request.user.id}")
        print(f"DEBUG: After login - User backend: {request.user.backend}")
        
        # Force session update
        request.session.modified = True
        
        # Clear OAuth session data
        request.session.pop('doing_oauth', None)
        request.session.pop('oauth_redirect_to', None)
        
        # Set minimal session data
        request.session['oauth_success'] = True
        request.session['user_email'] = user.email
        
        # CRITICAL: Save session to ensure authentication persists
        request.session.save()
        
        print(f"DEBUG: Session saved - Session key: {request.session.session_key}")
        print(f"DEBUG: Session saved - User ID in session: {request.session.get('_auth_user_id')}")
        print(f"DEBUG: Final check - User authenticated: {request.user.is_authenticated}")
        
        # Set additional session flags to ensure authentication persists
        request.session['user_authenticated'] = True
        request.session['user_id'] = user.id
        request.session['user_email'] = user.email
        request.session.save()
        
        print(f"DEBUG: Additional session data saved")
        print(f"DEBUG: ===== FINAL OAUTH CALLBACK STATE =====")
        print(f"DEBUG: User authenticated: {request.user.is_authenticated}")
        print(f"DEBUG: User email: {request.user.email}")
        print(f"DEBUG: User ID: {request.user.id}")
        print(f"DEBUG: Session keys: {list(request.session.keys())}")
        print(f"DEBUG: Session user ID: {request.session.get('_auth_user_id')}")
        print(f"DEBUG: Redirecting to dashboard")
        messages.success(request, f'Welcome {user.first_name}! You have successfully logged in.')
        
        # DIRECT redirect to dashboard - no conditions
        return HttpResponseRedirect('/dashboard/')
        
    except Exception as e:
        print(f"DEBUG: Microsoft OAuth callback error: {str(e)}")
        import traceback
        traceback.print_exc()
        print(f"DEBUG: Exception occurred - redirecting to dashboard anyway")
        # NEVER redirect to login - always dashboard
        return HttpResponseRedirect('/dashboard/')


def force_oauth_redirect_middleware(get_response):
    """
    MINIMAL middleware - just redirect authenticated users away from login
    """
    def middleware(request):
        # MINIMAL: If user is authenticated and on login page, force redirect to dashboard
        if (request.user.is_authenticated and 
            request.path == '/accounts/login/'):
            print(f"DEBUG: MINIMAL - Authenticated user {request.user.email} on login page, forcing redirect to dashboard")
            from django.http import HttpResponseRedirect
            return HttpResponseRedirect('/dashboard/')
        
        response = get_response(request)
        return response
    
    return middleware


def microsoft_oauth_complete(request):
    """
    AGGRESSIVE OAuth completion - NEVER redirects to login page
    """
    from social_django.views import complete
    from django.contrib.auth import login
    from django.http import HttpResponseRedirect
    
    try:
        print(f"DEBUG: AGGRESSIVE Microsoft OAuth completion started")
        print(f"DEBUG: User authenticated before completion: {request.user.is_authenticated}")
        
        # Call the original social_django complete view
        response = complete(request, 'azuread-tenant-oauth2')
        
        print(f"DEBUG: Social auth complete response - User authenticated: {request.user.is_authenticated}")
        print(f"DEBUG: Response type: {type(response)}")
        print(f"DEBUG: Response status: {getattr(response, 'status_code', 'No status')}")
        
        # ALWAYS redirect to dashboard for Microsoft OAuth users
        print(f"DEBUG: Microsoft OAuth completion - FORCING redirect to dashboard")
        
        # If user is authenticated, show success message and set session data
        if request.user.is_authenticated:
            messages.success(request, f'Welcome {request.user.first_name}! You have successfully logged in.')
            print(f"DEBUG: User {request.user.email} authenticated, redirecting to dashboard")
            
            # Set session data to prevent hijacking middleware from redirecting back to login
            request.session['ip_address'] = get_client_ip(request)
            request.session['user_agent'] = request.META.get('HTTP_USER_AGENT', '')
            request.session['session_token'] = request.session.session_key
            request.session['oauth_authenticated'] = True
            print(f"DEBUG: Set session data for OAuth user {request.user.email}")
        else:
            print(f"DEBUG: User not authenticated but forcing redirect anyway")
        
        # Clear any session flags
        request.session.pop('redirect_to_dashboard', None)
        
        # FORCE redirect to dashboard
        return HttpResponseRedirect('/dashboard/')
        
    except Exception as e:
        print(f"DEBUG: Microsoft OAuth completion error: {str(e)}")
        import traceback
        traceback.print_exc()
        print(f"DEBUG: Exception occurred - redirecting to dashboard anyway")
        # NEVER redirect to login - always dashboard
        return HttpResponseRedirect('/dashboard/')


def oauth_complete_redirect(request, backend):
    """
    AGGRESSIVE OAuth completion - NEVER redirects to login page
    """
    from social_django.views import complete
    from django.contrib.auth import login
    from django.http import HttpResponseRedirect
    
    try:
        print(f"DEBUG: AGGRESSIVE OAuth completion started for backend: {backend}")
        print(f"DEBUG: Session redirect_to_dashboard: {request.session.get('redirect_to_dashboard', False)}")
        
        # Call the original complete view
        response = complete(request, backend)
        
        print(f"DEBUG: OAuth complete response - User authenticated: {request.user.is_authenticated}")
        print(f"DEBUG: Response type: {type(response)}")
        print(f"DEBUG: Response status: {getattr(response, 'status_code', 'No status')}")
        
        # ALWAYS redirect to dashboard for OAuth users, regardless of authentication status
        if backend == 'azuread-tenant-oauth2':
            print(f"DEBUG: Microsoft OAuth detected - FORCING redirect to dashboard")
            
            # If user is authenticated, show success message and set session data
            if request.user.is_authenticated:
                messages.success(request, f'Welcome {request.user.first_name}! You have successfully logged in.')
                print(f"DEBUG: User {request.user.email} authenticated, redirecting to dashboard")
                
                # Set session data to prevent hijacking middleware from redirecting back to login
                request.session['ip_address'] = get_client_ip(request)
                request.session['user_agent'] = request.META.get('HTTP_USER_AGENT', '')
                request.session['session_token'] = request.session.session_key
                request.session['oauth_authenticated'] = True
                print(f"DEBUG: Set session data for OAuth user {request.user.email}")
            else:
                print(f"DEBUG: User not authenticated but forcing redirect anyway")
            
            # Clear any session flags
            request.session.pop('redirect_to_dashboard', None)
            
            # FORCE redirect to dashboard
            return HttpResponseRedirect('/dashboard/')
        
        return response
        
    except Exception as e:
        print(f"DEBUG: OAuth completion error: {str(e)}")
        import traceback
        traceback.print_exc()
        print(f"DEBUG: Exception occurred - redirecting to dashboard anyway")
        # NEVER redirect to login - always dashboard
        return HttpResponseRedirect('/dashboard/')


def login_with_tracking(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)

            # Save IP and browser info when logging in with OTP
            user.last_login_ip = get_client_ip(request)
            user.last_login_browser = request.META.get('HTTP_USER_AGENT', '')[:256]
            user.save(update_fields=['last_login_ip', 'last_login_browser'])
            return redirect(get_login_redirect_url(user))
    return render(request, 'accounts/sign-in.html')

# Email Verification (OtpToken model missing - commented out until model is created)
def verify_email(request, first_name):
    # user = get_user_model().objects.get(username=first_name)
    # user_otp = OtpToken.objects.filter(user=user).last()
    
    messages.info(request, "Email verification temporarily unavailable - OTP model missing")
    return redirect("login")
    
    # if request.method == 'POST':
    #     # valid token
    #     if user_otp.otp_code == request.POST['otp_code']:
    #         
    #         # checking for expired token
    #         if user_otp.otp_expires_at > timezone.now():
    #             user.is_active=True
    #             user.save()
    #             messages.success(request, "Account activated successfully!! You can Login.")
    #             return redirect("signin")
    #         
    #         # expired token
    #         else:
    #             messages.warning(request, "The OTP has expired, get a new OTP!")
    #             return redirect("verify-email", username=user.first_name)
    #     
    #     
    #     # invalid otp code
    #     else:
    #         messages.warning(request, "Invalid OTP entered, enter a valid OTP!")
    #         return redirect("verify-email", username=user.first_name)
    #     
    # context = {}
    # return render(request, "verify_token.html", context)


def resend_otp(request):
    # OtpToken model missing - function disabled until model is created
    messages.info(request, "OTP resend temporarily unavailable - OTP model missing")
    return redirect("login")
    
    # if request.method == 'POST':
    #     user_email = request.POST["otp_email"]
    #     
    #     if get_user_model().objects.filter(email=user_email).exists():
    #         user = get_user_model().objects.get(email=user_email)
    #         otp = OtpToken.objects.create(user=user, otp_expires_at=timezone.now() + timezone.timedelta(minutes=5))
    #         
    #         
    #         # email variables
    #         subject="Email Verification"
    #         message = f"""
    #                             Hi {user.username}, here is your OTP {otp.otp_code} 
    #                             it expires in 5 minute, use the url below to redirect back to the website
    #                             {request.build_absolute_uri(reverse('verify-email', args=[user.username]))}
    #                            
    #                             """
    #         sender = "kaviuln@gmail.com"
    #         receiver = [user.email, ]
    #     
    #     
    #         # send email
    #         send_mail(
    #                 subject,
    #                 message,
    #                 sender,
    #                 receiver,
    #                 fail_silently=False,
    #             )
    #         
    #         messages.success(request, "A new OTP has been sent to your email-address")
    #         return redirect("verify-email", username=user.first_name)
    # 
    #     else:
    #         messages.warning(request, "This email dosen't exist in the database")
    #         return redirect("resend-otp")
    #     
    #        
    # context = {}
    # return render(request, "resend_otp.html", context)



 
 
 
 
class UserPasswordResetView(PasswordResetView):
    template_name = 'accounts/password_reset.html'
    form_class = UserPasswordResetForm
 

class UserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    form_class = UserSetPasswordForm
 
class UserPasswordChangeView(PasswordChangeView):
    template_name = 'accounts/password_change.html'
    form_class = UserPasswordChangeForm
 
def resources_view(request):
    return render(request, 'pages/resources.html.')
   
def package_plan(request):
    return render(request, 'pages/package-plan.html')
 
@staff_member_required  
def admin_dashboard(request):
    """
    Admin dashboard view with session management.
    """
    # Verify user has admin privileges
    if not request.user.is_admin_user():
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('login')

    # Check if this is a valid admin session
    is_admin_session = request.session.get('is_admin_session', False)
    if not is_admin_session:
        messages.warning(request, 'Please log in through the admin portal.')
        return redirect('admin_login')

    return render(request, 'admin/dashboard.html', {
        'user': request.user,
        'admin_session_active': True
    })


# Chart Views
 
@staff_member_required
def get_filter_options(request):
    return JsonResponse({
        "options": ['p1', 'p2', 'p3']
    })
 
@staff_member_required
def get_priority_breakdown(request, priority):
    students = Student.objects.all()
    project_titles = list(Project.objects.all().values('title').order_by()) # list of dictionaries: [{'title': 'AppAttack'}, {'title': 'Malware Visualization'},...
 
    project_count = students.values(f'{priority}__title').annotate(dcount=Count('p1')).order_by()
 
    return JsonResponse({
        'title': f'Projects on {priority}',
        'data': {
            'labels': [d['title'] for d in project_titles],
            'datasets': [{
                'label': 'Students',
                'backgroundColor': generate_color_palette(len(project_titles)),
                'borderColor': generate_color_palette(len(project_titles)),
                'data': [p['dcount'] for p in project_count]
            }]
        }
    })

import base64

def blogpage(request):
    if request.method == 'POST':
        form = UserBlogPageForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)

            # Ensure 'isShow' is set to False by default
            blog.isShow = False  # Default value is False, no need to check

            uploaded_file = request.FILES.get('file')
            if uploaded_file:
                blog.file = base64.b64encode(uploaded_file.read()).decode('utf-8')

            blog.save()
            return redirect('blogpage')
    else:
        form = UserBlogPageForm()

    blogpages = UserBlogPage.objects.all().order_by('-created_at')[:10]
    return render(request, 'pages/blogpage.html', {'form': form, 'blogpages': blogpages})


def edit_blogpage(request, id):
    blog = get_object_or_404(UserBlogPage, id=id)

    if request.method == 'POST':
        blog.name = request.POST.get('name')
        blog.title = request.POST.get('title')
        blog.description = request.POST.get('description')
        uploaded_file = request.FILES.get('file')
        if uploaded_file:
         blog.file = base64.b64encode(uploaded_file.read()).decode('utf-8')
        blog.save()
        return redirect('blogpage')

    return render(request, 'pages/blogpage.html', {'blog': blog})
 
def blogpage_view(request):
    if request.method == 'POST':
        form = UserBlogPageForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('blogpage')
    else:
        form = UserBlogPageForm()

    blogpages = UserBlogPage.objects.all().order_by('-created_at')
    return render(request, 'blogpage.html', {
        'form': form,
        'blogpages': blogpages
    })

def delete_blogpage(request, id):
    blogpage= get_object_or_404(UserBlogPage, id=id)
    blogpage.delete()
    return redirect('blogpage')

def adminblogpage(request):
    blogpages = UserBlogPage.objects.all().order_by('-created_at')
    return render(request, 'pages/adminblogpage.html', {'blogpages': blogpages})

def approve_blogpage(request, id):
    blog = get_object_or_404(UserBlogPage, id=id)
    blog.isShow = True
    blog.save()
    return redirect('adminblogpage')

def reject_blogpage(request, id):
    blog = get_object_or_404(UserBlogPage, id=id)
    blog.delete()
    return redirect('adminblogpage')

def publishedblog(request):
    blogpages = UserBlogPage.objects.filter(isShow=True).order_by('-created_at')
    return render(request, 'pages/publishedblog.html', {'blogpages': blogpages})

def report_blog(request):
    if request.method == 'POST':
        blog_id = request.POST.get('blog_id')
        blog_name = request.POST.get('blog_name')
        reason = request.POST.get('reason')

        print(f"Blog ID: {blog_id}")
        print(f"Blog Name: {blog_name}")
        print(f"Report Reason: {reason}")

        # Save the report to the database
        Report.objects.create(
            blog_id=blog_id,
            blog_name=blog_name,
            reason=reason
        )

        messages.success(request, "Thanks for reporting the blog.")
        return redirect('publishedblog')

    # Optional fallback for non-POST requests
    messages.warning(request, "Invalid request.")
    return redirect('publishedblog')

def adminblogreports(request):
    reports = Report.objects.all().order_by('-created_at')
    return render(request, 'pages/reports.html', {'reports': reports})

import csv
from django.http import HttpResponse

def download_reported_blogs(request):
    reports = Report.objects.all()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="reported_blogs.csv"'

    writer = csv.writer(response)
    writer.writerow(['#', 'Blog ID', 'Blog Name', 'Reason', 'Date'])

    for idx, report in enumerate(reports, start=1):
        writer.writerow([
            idx,
            report.blog_id,
            report.blog_name,
            report.reason,
            report.created_at.strftime('%Y-%m-%d %H:%M')
        ])

    return response
    
def statistics_view(request):
    return render(request, 'charts/statistics.html')
 
def comphrehensive_reports(request):
    # Page from the theme
    return render(request, 'pages/appattack/comprehensive_reports.html')
 
def pen_testing(request):
    # Page from the theme
    return render(request, 'pages/appattack/pen_testing.html')
 
def secure_code_review(request):
    # Page from the theme
    return render(request, 'pages/appattack/secure_code_review.html')
 
# @login_required  # TEMPORARILY DISABLED TO TEST AUTHENTICATION
def dashboard(request):
    print(f"DEBUG: ===== DASHBOARD VIEW CALLED =====")
    print(f"DEBUG: Request path: {request.path}")
    print(f"DEBUG: Request method: {request.method}")
    print(f"DEBUG: User authenticated: {request.user.is_authenticated}")
    print(f"DEBUG: User email: {request.user.email if request.user.is_authenticated else 'Not authenticated'}")
    print(f"DEBUG: User ID: {request.user.id if request.user.is_authenticated else 'No ID'}")
    print(f"DEBUG: Session keys: {list(request.session.keys())}")
    print(f"DEBUG: User ID in session: {request.session.get('_auth_user_id')}")
    print(f"DEBUG: User email in session: {request.session.get('user_email')}")
    print(f"DEBUG: User authenticated flag in session: {request.session.get('user_authenticated')}")
    
    # Check if user is authenticated
    if not request.user.is_authenticated:
        print(f"DEBUG: User not authenticated, but continuing to show dashboard anyway")
        # Don't redirect - just show dashboard with anonymous user
    
    user = request.user
    
    # Handle anonymous user case
    if not user.is_authenticated:
        print(f"DEBUG: Handling anonymous user in dashboard")
        
        # Try to restore user from session data
        user_id = request.session.get('user_id')
        user_email = request.session.get('user_email')
        
        if user_id and user_email:
            print(f"DEBUG: Found session data - User ID: {user_id}, Email: {user_email}")
            try:
                from django.contrib.auth import get_user_model
                User = get_user_model()
                user = User.objects.get(id=user_id, email=user_email)
                print(f"DEBUG: Restored user from session: {user.email}")
                
                # Try to manually authenticate the user
                from django.contrib.auth import login
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request, user)
                print(f"DEBUG: Manually logged in user: {user.email}")
                print(f"DEBUG: User authenticated after manual login: {request.user.is_authenticated}")
                
                student = Student.objects.filter(user=user).first()
            except User.DoesNotExist:
                print(f"DEBUG: Could not restore user from session")
                # Create a mock user object for anonymous users
                class AnonymousUserData:
                    def __init__(self):
                        self.email = "anonymous@example.com"
                        self.first_name = "Anonymous"
                        self.last_name = "User"
                        self.is_authenticated = False
                
                user = AnonymousUserData()
                student = None
        else:
            print(f"DEBUG: No session data found")
            # Create a mock user object for anonymous users
            class AnonymousUserData:
                def __init__(self):
                    self.email = "anonymous@example.com"
                    self.first_name = "Anonymous"
                    self.last_name = "User"
                    self.is_authenticated = False
            
            user = AnonymousUserData()
            student = None
    else:
        print(f"DEBUG: User is authenticated: {user.email}")
        student = Student.objects.filter(user=user).first()

    skills = [
        {'title': 'Docker Basics', 'slug': 'docker-basics'},
        {'title': 'HTML & Tailwind Styling', 'slug': 'html-tailwind'},
        {'title': 'Git & GitHub Workflows', 'slug': 'git-github-workflows'},
        {'title': 'Django', 'slug': 'django'},
        {'title': 'Secure Code Review', 'slug': 'secure-code-review'},
    ]

    # Handle progress data for anonymous users
    if hasattr(user, 'upskilling_progress'):
        progress_data = user.upskilling_progress or {}
    else:
        progress_data = {}

    completed = in_progress = not_started = 0

    for skill in skills:
        status = progress_data.get(skill['slug'], 'Not Started')
        skill['status'] = status
        if status == 'Completed':
            completed += 1
        elif status == 'In Progress':
            in_progress += 1
        else:
            not_started += 1

    total = len(skills)
    percent = round((completed / total) * 100) if total > 0 else 0

    return render(request, 'pages/dashboard.html', {
        'user': user,
        'student': student,
        'skills': skills,
        'completed_count': completed,
        'in_progress_count': in_progress,
        'not_started_count': not_started,
        'percent': percent,
        'total': total,
    })

 
def update_progress(request, progress_id):
    progress = get_object_or_404(Progress, id=progress_id)
    if request.method == 'POST':
        data = json.loads(request.body)
        new_progress = data.get('progress')
 
        print(f'Received new_progress: {new_progress}')  # Debugging line
 
        if new_progress is None:
            new_progress = 0
        else:
            new_progress = int(new_progress)
 
        progress.progress = new_progress
        progress.save()
 
        print(f'Saved new_progress: {progress.progress}')  # Debugging line
 
        return JsonResponse({'status': 'success'})
 
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
 
def contact(request):
    if request.method=='POST':
        name=request.POST.g['name']
        email=request.POST['email']
        message=request.POST['message']
        contact=Contact.objects.create(name=name, email=email, message=message)
        messages.success(request,'The message has been received')

        
    return render(request,'pages/index.html')
 
#For XSS Log
xss_logger = logging.getLogger('xss_logger')
xss_logger.warning("List of latest XSS attacks detection: ")

def log_suspicious_input(input_data):
    if input_data and "<script>" in input_data.lower():
        xss_logger.warning(f"XSS Attack Detected: {input_data}")
        print(f"XSS attempt full message: {input_data}") 

#For Contact Page
def Contact_central(request):

    if request.method=='POST':
        name=request.POST['name']
        email=request.POST['email']
        message=request.POST['message']
        contact=Contact.objects.create(name=name, email=email, message=message)
        messages.success(request,'The message has been received')

        try:
            send_mail(
                subject=f"Thank you, {name}, for contacting us!",
                message=f"Dear {name},\n\nThank you for your message:\n\n\"{message}\"\n\nWe will get back to you shortly.\n\nBest regards,\nYour Team",
                from_email='hardhatcompanywebsite@gmail.com',
                recipient_list=[email],
                fail_silently=False,
            )
        except Exception as e:
            messages.error(request, 'Failed to send confirmation email.')
    return render(request,'pages/Contactus.html')

    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        message = request.POST.get('message', '')

        print(f"Name: {name}, Email: {email}, Message: {message}")

        # Log suspicious inputs of Contact
        log_suspicious_input(name)
        log_suspicious_input(email)
        log_suspicious_input(message)

        # Sanitizing and validating inputs
        name = nh3.clean(xss_detection(name))
        email = nh3.clean(xss_detection(email))
        message = nh3.clean(xss_detection(message))

        if name and email and message:
            Contact.objects.create(name=name, email=email, message=message)
            messages.success(request, 'Message has been sent successfully!')
        else:
            messages.error(request, 'Invalid input!')

    return render(request, 'pages/Contactus.html')

def generate_and_send_passkeys(user):
    # Generate 5 permanent passkeys
    passkeys = [Passkey.generate_passkey() for _ in range(5)]

    # Save to database (without expiration)
    for key in passkeys:
        Passkey.objects.create(user=user, key=key)

    # Email the passkeys to the user
    send_mail(
        subject="Your Permanent HardHat Enterprise Passkeys",
        message=(
            f"Hello {user.first_name},\n\n"
            "Here are your permanent login passkeys:\n"
            f"{', '.join(passkeys)}\n\n"
            "Each passkey can be used at any time instead of OTP during login.\n"
            "Keep them safe!\n\nRegards,\nHardHat Enterprises"
        ),
        from_email="deakinhardhatwebsite@gmail.com",
        recipient_list=[user.email],
        fail_silently=False,
    )

    print(f"DEBUG MODE: Lifetime Passkeys for {user.email}: {passkeys}")  # Debugging
 
# Blog
class Index(ListView):
    model = Article
    queryset = Article.objects.all().order_by('-date')
    template_name = 'blog/index.html'
    paginate_by = 1
 
class DetailArticleView(DetailView):
    model = Article
    template_name = 'blog/blog_post.html'
 
    def get_context_data(self, *args, **kwargs):
        context = super(DetailArticleView, self).get_context_data(*args, **kwargs)
        context['liked_by_user']  = False  
        article = Article.objects.get(id=self.kwargs.get('pk'))    
        if article.likes.filter(pk=self.request.user.id).exists():
            context['liked_by_user']  = True
        return context
 
class LikeArticle(View):
    def post(self, request, pk):
        article = Article.objects.get(id=pk)
        if article.likes.filter(pk=self.request.user.id).exists():
            article.likes.remove(request.user.id)
        else:
            article.likes.add(request.user.id)
        article.save()
        return redirect('detail_article', pk)
 
class UpskillingView(LoginRequiredMixin, ListView):
    login_url = '/accounts/login/'
    model = Skill
    template_name = 'pages/upskilling.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Retrieve the user's saved upskilling progress from the database
        progress_data = self.request.user.upskilling_progress or {}

        # Define the list of skills
        context['skills'] = [
            {
                'title': 'Docker Basics',
                'slug': 'docker-basics',
                'difficulty': 'Beginner',
                'tags': ['DevOps', 'Containers'],
                'status': progress_data.get('docker-basics', 'Not Started')
            },
            {
                'title': 'HTML & Tailwind Styling',
                'slug': 'html-tailwind',
                'difficulty': 'Beginner',
                'tags': ['Frontend', 'UI', 'CSS'],
                'status': progress_data.get('html-tailwind', 'Not Started')
            },
            {
                'title': 'Git & GitHub Workflows',
                'slug': 'git-github-workflows',
                'difficulty': 'Intermediate',
                'tags': ['Collaboration', 'Version Control'],
                'status': progress_data.get('git-github-workflows', 'Not Started')
            },
            {
                'title': 'Django',
                'slug': 'django',
                'difficulty': 'Intermediate',
                'tags': ['Python', 'Web Dev'],
                'status': progress_data.get('django', 'Not Started')
            },
            {
                'title': 'Secure Code Review',
                'slug': 'secure-code-review',
                'difficulty': 'Advanced',
                'tags': ['Security', 'Code Quality'],
                'status': progress_data.get('secure-code-review', 'Not Started')
            }
        ]

        return context

    def get_queryset(self):
        if self.request.user.is_authenticated:
            student = Student.objects.filter(user=self.request.user).first()
            progress = Progress.objects.filter(student=student)
            return [p.skill for p in progress]
        else:
            return self.model.objects.none()



class UpskillingSkillView(LoginRequiredMixin, DetailView):
    login_url = '/accounts/login/'  
    model = Skill
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        progress = request.user.upskilling_progress or {}

        if progress.get(slug) != "Completed":
            progress[slug] = "In Progress"
            request.user.upskilling_progress = progress
            request.user.save()

        return super().get(request, *args, **kwargs)

    def get_template_names(self):
        return [f'pages/upskilling/{self.kwargs["slug"]}_skill.html']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            student = Student.objects.filter(user=self.request.user).first()
            if student:
                progress = Progress.objects.filter(student=student, skill=self.object).first()
                if progress:
                    context['progress_id'] = progress.id

        return context

    def get_object(self):
        dummy_skills = [
            {
                'title': 'Docker Basics',
                'slug': 'docker-basics',
                'difficulty': 'Beginner',
                'tags': ['DevOps', 'Containers'],
                'status': 'Not Started'
            },
            {
                'title': 'HTML & Tailwind Styling',
                'slug': 'html-tailwind',
                'difficulty': 'Beginner',
                'tags': ['Frontend', 'UI', 'CSS'],
                'status': 'Not Started'
            },
            {
                'title': 'Git & GitHub Workflows',
                'slug': 'git-github-workflows',
                'difficulty': 'Intermediate',
                'tags': ['Collaboration', 'Version Control'],
                'status': 'Completed'
            },
            {
                'title': 'Django',
                'slug': 'django',
                'difficulty': 'Intermediate',
                'tags': ['Python', 'Web Dev'],
                'status': 'Not Started'
            },
            {
                'title': 'Secure Code Review',
                'slug': 'secure-code-review',
                'difficulty': 'Advanced',
                'tags': ['Security', 'Code Quality'],
                'status': 'In Progress'
            }
        ]

        for skill in dummy_skills:
            if skill['slug'] == self.kwargs['slug']:
                return skill

        raise Http404("Skill not found")


class MarkSkillCompletedView(LoginRequiredMixin, View):
    def post(self, request, slug):
        user = request.user
        progress = user.upskilling_progress or {}

        # Mark the skill as completed
        progress[slug] = "Completed"
        user.upskilling_progress = progress
        user.save()

        return redirect('upskilling')  # send them back to dashboard

class UserPasswordResetView(PasswordResetView):
    template_name = 'accounts/password_reset.html'
    form_class = UserPasswordResetForm

    def form_valid(self, form):
        email = form.cleaned_data['email']
        users = get_user_model().objects.filter(email=email)
        if users.exists():
            for user in users:
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)
                reset_url = self.request.build_absolute_uri(
                    reverse_lazy('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
                )
                subject = 'Password Reset'
                message = (
                    f"You're receiving this email because you have requested a password reset for your user account at {self.request.META['HTTP_HOST']}.\n\n"
                    f"Please go to the following page and choose a new password:\n{reset_url}\n\n"
                    "If you didn't request a password reset, please contact us at your earliest convenience.\n\n"
                    "Regards,\nHardhat Enterprises"
                )
            send_mail(subject, message, 'deakinhardhatwebsite@gmail.com', [email], fail_silently=False)
            return redirect('password_reset_done')
        else:
            messages.error(self.request, "User does not exist. Please enter a valid email address.")
            return self.form_invalid(form)


def vr_join_us(request):
    return projects_join_us(request, 'pages/Vr/join_us.html', 'cybersafe_vr_join_us')

def cyber_threat_simulation(request):
    return render(request, 'pages/Vr/cyber_threat_simulation.html')

def secure_digital_practices(request):
    return render(request, 'pages/Vr/secure_digital_practices.html')

def cybersecurity_awareness_reports(request):
    return render(request, 'pages/Vr/cybersecurity_awareness_reports.html')

def Deakin_Threat_mirror_joinus(request):
    return projects_join_us(request, 'pages/DeakinThreatmirror/join_us.html', 'threat_mirror_join_us')

def projects_join_us(request, page_url, page_name):
    if request.method == 'POST':
        # Copy of POST data 
        post_data = request.POST.copy()
        # Set the page_name value 
        post_data['page_name'] = page_name
        # Form with the modified POST data
        form = projects_JoinUsForm(post_data)
        print(form)
        if form.is_valid():
            form.save()
            messages.success(request, "Your message has been successfully sent")
            return redirect(page_name) 
        else:
            print(request)
            messages.error(request, "Please fill the form correctly")
    else:
        form = projects_JoinUsForm(initial={'page_name': page_name})
    print(request)
    return render(request, page_url, {'form': form, 'page_name': page_name})

def feedback_view(request):
    sentiment = None
    name = None
    rating = None

    if request.method == 'POST':
        post_data = request.POST.copy()  # Make a mutable copy
        if 'anonymous' in post_data:
            post_data['name'] = 'Anonymous'

        form = ExperienceForm(post_data)  # Use modified post_data

        if form.is_valid():
            feedback_obj = form.save(commit=False)
            feedback_text = form.cleaned_data.get('feedback')
            name = form.cleaned_data.get('name')
            rating = post_data.get('rating')  # ⭐️ Rating from hidden/radio field

            # 🧠 Sentiment analysis
            blob = TextBlob(feedback_text)
            polarity = blob.sentiment.polarity

            if polarity >= 0.1:
                sentiment = "positive"
            elif polarity <= -0.1:
                sentiment = "negative"
            else:
                sentiment = "neutral"

            # ⭐️ Save rating if present
            if rating:
                feedback_obj.rating = int(rating)

            feedback_obj.save()

            # 📊 Calculate average rating and total number of ratings
            aggregate = Experience.objects.aggregate(
                avg=Avg('rating'),
                count=Count('rating')
            )
            average_rating = round(aggregate['avg'] or 0, 1)
            rating_count = aggregate['count']

            return render(request, 'feedback/thank_you.html', {
                'name': name,
                'sentiment': sentiment,
                'rating': int(rating) if rating else None,
                'average_rating': average_rating,
                'rating_count': rating_count
            })
    else:
        form = ExperienceForm()

    # 📥 Fetch all past feedback
    feedbacks = Experience.objects.all().order_by('-created_at')

    return render(request, 'pages/feedback.html', {
        'form': form,
        'feedbacks': feedbacks
    })
    
def delete_feedback(request, id):
    feedback= get_object_or_404(Experience, id=id)
    feedback.delete()
    return redirect('feedback')

def challenge_list(request):
    categories = CyberChallenge.objects.values('category').annotate(count=Count('id')).order_by('category')
    
    # Check if user is staff or superuser
    show_admin_controls = request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser)

    return render(request, 'pages/challenges/challenge_list.html', {
        'categories': categories,
        'show_admin_controls': show_admin_controls
    })

def cyber_challenge(request):
    """
    View for the cyber challenge page with admin controls.
    """
    # Check if user is staff or superuser
    show_admin_controls = request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser)

    return render(request, 'cyber_challenge.html', {
        'show_admin_controls': show_admin_controls
    })


@login_required
def category_challenges(request, category):
    challenges = CyberChallenge.objects.filter(category=category).order_by('difficulty')
    completed_challenges = UserChallenge.objects.filter(user=request.user, completed=True).values_list('challenge_id', flat=True)
    return render(request, 'pages/challenges/category_challenges.html', {'category': category, 'challenges': challenges, 'completed_challenges': completed_challenges})

import sys
import io
import contextlib
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import CyberChallenge, UserChallenge

@login_required
def challenge_detail(request, challenge_id):
    challenge = get_object_or_404(CyberChallenge, id=challenge_id)
    next_challenge = CyberChallenge.objects.filter(category=challenge.category, id__gt=challenge.id).order_by('id').first()
    user_challenge, created = UserChallenge.objects.get_or_create(user=request.user, challenge=challenge)

    if request.method == 'POST':
        # For MCQ (Multiple Choice Question) challenges
        if challenge.challenge_type == 'mcq':
            selected = request.POST.get("selected_choice", "").strip()
            correct_answer = challenge.correct_answer.strip()

            # Handle JSON array format for correct_answer
            try:
                import json
                parsed_correct = json.loads(correct_answer)
                if isinstance(parsed_correct, list):
                    # If correct_answer is a JSON array, check if user_answer matches any element
                    is_correct = selected in parsed_correct
                else:
                    # If it's not a list, compare directly
                    is_correct = selected == correct_answer
            except (json.JSONDecodeError, TypeError):
                # If it's not valid JSON, compare directly
                is_correct = selected == correct_answer
            
            user_challenge.completed = is_correct
            user_challenge.score = challenge.points if is_correct else 0
            
            if is_correct:
                output = "Correct!"
            else:
                output = "Incorrect. The correct answer is: " + correct_answer

        # For Fix the Code challenges
        elif challenge.challenge_type == 'fix_code':
            user_code = request.POST.get("code_input", "").strip()
            correct_code = challenge.correct_answer.strip()
            
            # Compare the user's code directly with the correct answer code
            is_correct = user_code.strip() == correct_code.strip()
            output = "Code comparison completed"
            user_challenge.completed = is_correct
            user_challenge.score = challenge.points if is_correct else 0

        user_challenge.save()

        return JsonResponse({
            'is_correct': user_challenge.completed,
            'message': 'Correct!' if user_challenge.completed else 'Incorrect.',
            'explanation': challenge.explanation,
            'output': output,
            'score': user_challenge.score
        })

    return render(request, 'pages/challenges/challenge_detail.html', {
        'challenge': challenge,
        'next_challenge': next_challenge,
        'user_challenge': user_challenge,
    })


@login_required
def submit_answer(request, challenge_id):
    if request.method == 'POST':
        challenge = get_object_or_404(CyberChallenge, id=challenge_id)
        user_answer = request.POST.get('selected_choice', '')  
        user_code = request.POST.get('code_input', '')  
        output = ""
        is_correct = False
        explanation = challenge.explanation or ""

        if challenge.challenge_type == 'mcq':
            correct_answer = challenge.correct_answer.strip()
            user_answer = user_answer.strip()
            
            # Handle JSON array format for correct_answer
            try:
                import json
                parsed_correct = json.loads(correct_answer)
                if isinstance(parsed_correct, list):
                    # If correct_answer is a JSON array, check if user_answer matches any element
                    is_correct = user_answer in parsed_correct
                else:
                    # If it's not a list, compare directly
                    is_correct = user_answer == correct_answer
            except (json.JSONDecodeError, TypeError):
                # If it's not valid JSON, compare directly
                is_correct = user_answer == correct_answer
            
            if is_correct:
                output = "Correct!"
            else:
                output = "Incorrect. The correct answer is: " + correct_answer

        elif challenge.challenge_type == 'fix_code':
            user_code = request.POST.get('code_input', '').strip()
            correct_code = challenge.correct_answer.strip()
            
            # Compare the user's code directly with the correct answer code
            is_correct = user_code.strip() == correct_code.strip()
            output = "Code comparison completed"
            user_challenge.completed = is_correct
            user_challenge.score = challenge.points if is_correct else 0

        user_challenge, created = UserChallenge.objects.get_or_create(user=request.user, challenge=challenge)

        user_challenge.completed = is_correct
        user_challenge.score = challenge.points if is_correct else 0
        user_challenge.save()
        
        # If challenge is correct, update the leaderboard
        if is_correct:
            user_challenge.completed = True
            user_challenge.score = challenge.points
            user_challenge.save()
            # Calculate total points
            total_points = UserChallenge.objects.filter(
                user=request.user,
                challenge__category=challenge.category
            ).aggregate(Sum('score'))['score__sum'] or 0

            # Update leaderboard
            leaderboard_entry, created = LeaderBoardTable.objects.get_or_create(
                user=request.user,
                category=challenge.category
            )
            leaderboard_entry.total_points = total_points
            leaderboard_entry.save()

        return JsonResponse({
            'is_correct': is_correct,
            'message': "Correct!" if is_correct else "Try again",
            'explanation': explanation,
            'output': output,
            'score': challenge.points if is_correct else 0
        })

    return JsonResponse({'error': 'Invalid request'}, status=400)


#
def blog_list(request):
    # Initial blog post rendering (first page)
    posts = BlogPost.objects.all().order_by('-created_at')
    paginator = Paginator(posts, 5)  # 5 posts per page

    # Page number from request (default to 1)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    # Non-AJAX request: initial page load
    if not request.is_ajax():
        return render(request, 'blog_list.html', {'page_obj': page_obj})

    # AJAX request: send paginated posts as JSON
    posts_html = render_to_string('posts_partial.html', {'page_obj': page_obj})
    return JsonResponse({'posts_html': posts_html, 'has_next': page_obj.has_next()})

def list_careers(request):
    jobs = Job.objects.filter(closing_date__gte=timezone.now()).order_by('closing_date')

    search = request.GET.get('search', '')
    job_type = request.GET.get('job_type', '')
    location = request.GET.get('location', '')

    if search:
        jobs = jobs.filter(Q(title__icontains=search) | Q(description__icontains=search))
    if job_type:
        jobs = jobs.filter(job_type=job_type)
    if location:
        jobs = jobs.filter(location=location)

    context = {
        "jobs": jobs,
    }

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, "careers/partials/job-listings.html", context)
    else:
        return render(request, "careers/career-list.html", context)


def career_detail(request,id):
    job = get_object_or_404(Job, id=id)
    context = {
        "job":job
    }
    return render(request,"careers/career-detail.html",context)

def career_discover(request):
    return render(request, "careers/discover.html")

def internships(request):
    internships = Job.objects.filter(job_type='internship', closing_date__gte=timezone.now()).order_by('closing_date')
    context = {
        "internships": internships
    }
    return render(request, "careers/internships.html", context)

# View for Job Alerts Page
def job_alerts(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            # Check if email already exists
            job_alert, created = JobAlert.objects.get_or_create(email=email)
            if created:
                # Send confirmation email
                job_alert.send_confirmation_email()
                messages.success(request, 'Successfully subscribed to job alerts! Check your email for confirmation.')
            else:
                if job_alert.is_active:
                    messages.info(request, 'You are already subscribed to job alerts.')
                else:
                    job_alert.is_active = True
                    job_alert.save()
                    job_alert.send_confirmation_email()
                    messages.success(request, 'Successfully re-subscribed to job alerts! Check your email for confirmation.')
        else:
            messages.error(request, 'Please provide a valid email address.')
    
    return render(request, "careers/job-alerts.html")

def career_path_finder(request):
    return render(request, "careers/path_finder.html")

def career_application(request,id):
    job = get_object_or_404(Job, id=id)
    complete =False
    if request.method == 'POST':
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            JobApplication.objects.create(
                job_id=job.id,
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                resume=form.cleaned_data['resume'],
                cover_letter=form.cleaned_data['cover_letter']
            )
            complete=True
            # return redirect('career_list')
    else:
        form = JobApplicationForm()
    context = {
        "form":form,
        "job":job,
        "complete":complete
    }
    return render(request,"careers/application-form.html",context)

def graduate_program(request):
    """View for the Graduate Program roadmap page"""
    return render(request, "careers/graduate-program.html")



def careers_faqs(request):
    """View for the Careers FAQ page"""
    return render(request, "careers/faqs.html")

  
#swagger-implementation

class APIModelListView(APIView):

    @swagger_auto_schema(
        operation_summary="List API Models",
        operation_description="Retrieve a list of all API models in the system.",
        responses={
            200: APIModelSerializer(many=True),
            401: 'Authentication required',
            403: 'Permission denied'
        },
        tags=["API Models"]
    )

    def get(self, request):
        data = APIModel.objects.all()
        serializer = APIModelSerializer(data, many=True)
        return Response(serializer.data)
    
class AnalyticsAPI(APIView):
    @swagger_auto_schema(
        operation_summary="Fetch Analytics Data",
        operation_description="Retrieve analytics data including user statistics, challenge completions, and system metrics.",
        responses={
            200: openapi.Response(
                description="Analytics data retrieved successfully",
                examples={
                    "application/json": {
                        "total_users": 150,
                        "active_challenges": 25,
                        "completed_challenges": 1200,
                        "total_points_awarded": 50000,
                        "last_updated": "2024-01-15T10:30:00Z"
                    }
                }
            ),
            401: 'Authentication required',
            403: 'Permission denied'
        },

        tags=["Analytics"]  
    )
    def get(self, request):
        # Get basic analytics data
        total_users = User.objects.count()
        active_challenges = CyberChallenge.objects.filter(is_active=True).count()
        completed_challenges = UserChallenge.objects.filter(completed=True).count()
        total_points = UserChallenge.objects.filter(completed=True).aggregate(
            total=Sum('score')
        )['total'] or 0
        
        analytics_data = {
            "total_users": total_users,
            "active_challenges": active_challenges,
            "completed_challenges": completed_challenges,
            "total_points_awarded": total_points,
            "last_updated": timezone.now().isoformat()
        }
        
        return Response(analytics_data)   
    
class UserManagementAPI(APIView):
    @swagger_auto_schema(
        operation_summary="Get User Details",
       operation_description="Retrieve detailed information of the authenticated user including profile, progress, and achievements.",
        responses={
            200: openapi.Response(
                description="User details retrieved successfully",
                examples={
                    "application/json": {
                        "id": 1,
                        "email": "john@example.com",
                        "first_name": "John",
                        "last_name": "Doe",
                        "is_active": True,
                        "profile": {
                            "bio": "Cybersecurity enthusiast",
                            "avatar": "/media/avatars/user1.jpg"
                        },
                        "completed_challenges": 15,
                        "total_points": 2500,
                        "rank": 5
                    }
                }
            ),
            401: 'Authentication required',
            403: 'Permission denied'
        },

        tags=["User Management"]  
    )
    def get(self, request):
        if not request.user.is_authenticated:
            return Response({"error": "Authentication required"}, status=401)
        
        user = request.user
        completed_challenges = UserChallenge.objects.filter(user=user, completed=True).count()
        total_points = UserChallenge.objects.filter(user=user, completed=True).aggregate(
            total=Sum('score')
        )['total'] or 0
        
        # Get user's rank (simplified)
        user_rank = LeaderBoardTable.objects.filter(
            user=user
        ).aggregate(rank=Count('id'))['rank'] or 0
        
        user_data = {
            "id": user.id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "is_active": user.is_active,
            "completed_challenges": completed_challenges,
            "total_points": total_points,
            "rank": user_rank
        }
        
        # Add profile data if exists
        try:
            profile = user.profile
            user_data["profile"] = {
                "bio": profile.bio,
                "avatar": profile.avatar.url if profile.avatar else None
            }
        except:
            user_data["profile"] = None
        
        return Response(user_data)    
    
class EmailNotificationViewSet(ViewSet):
    @swagger_auto_schema(
        operation_summary="Send Email Notification",
        operation_description="Send a notification email to a user with customizable content and recipients.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['recipient_email', 'subject', 'message'],
            properties={
                'recipient_email': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    format=openapi.FORMAT_EMAIL,
                    description='Email address of the recipient'
                ),
                'subject': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Subject line of the email'
                ),
                'message': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Content of the email message'
                ),
                'notification_type': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    enum=['info', 'warning', 'success', 'error'],
                    description='Type of notification',
                    default='info'
                )
            }
        ),
        responses={
            201: openapi.Response(
                description="Email notification sent successfully",
                examples={
                    "application/json": {
                        "message": "Email sent successfully!",
                        "notification_id": "notif_123456",
                        "sent_at": "2024-01-15T10:30:00Z"
                    }
                }
            ),
            400: 'Invalid request data',
            401: 'Authentication required',
            403: 'Permission denied'
        },

        tags=["Email Notifications"]  
    )
    def create(self, request):
        recipient_email = request.data.get('recipient_email')
        subject = request.data.get('subject')
        message = request.data.get('message')
        notification_type = request.data.get('notification_type', 'info')
        
        if not all([recipient_email, subject, message]):
            return Response(
                {"error": "Missing required fields: recipient_email, subject, message"}, 
                status=400
            )
        
        # In a real implementation, you would send the actual email here
        # For now, we'll just return a success response
        notification_id = f"notif_{random.randint(100000, 999999)}"
        
        return Response({
            "message": "Email sent successfully!",
            "notification_id": notification_id,
            "sent_at": timezone.now().isoformat()
        }, status=201)


# Additional API endpoints for comprehensive documentation

class ChallengeListAPI(APIView):
    """
    API endpoint to list cybersecurity challenges.
    """
    @swagger_auto_schema(
        operation_summary="List Cybersecurity Challenges",
        operation_description="Retrieve a list of all available cybersecurity challenges with filtering options.",
        manual_parameters=[
            openapi.Parameter(
                'difficulty',
                openapi.IN_QUERY,
                description="Filter by difficulty level",
                type=openapi.TYPE_STRING,
                enum=['easy', 'medium', 'hard']
            ),
            openapi.Parameter(
                'category',
                openapi.IN_QUERY,
                description="Filter by challenge category",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'is_active',
                openapi.IN_QUERY,
                description="Filter by active status",
                type=openapi.TYPE_BOOLEAN
            )
        ],
        responses={
            200: openapi.Response(
                description="Challenges retrieved successfully",
                examples={
                    "application/json": {
                        "count": 25,
                        "results": [
                            {
                                "id": 1,
                                "title": "SQL Injection Challenge",
                                "description": "Identify and exploit SQL injection vulnerabilities",
                                "difficulty": "medium",
                                "category": "web_security",
                                "points": 100,
                                "is_active": True,
                                "created_at": "2024-01-01T00:00:00Z"
                            }
                        ]
                    }
                }
            ),
            401: 'Authentication required'
        },
        tags=["Challenges"]
    )
    def get(self, request):
        challenges = CyberChallenge.objects.all()
        
        # Apply filters
        difficulty = request.query_params.get('difficulty')
        category = request.query_params.get('category')
        is_active = request.query_params.get('is_active')
        
        if difficulty:
            challenges = challenges.filter(difficulty=difficulty)
        if category:
            challenges = challenges.filter(category=category)
        if is_active is not None:
            challenges = challenges.filter(is_active=is_active.lower() == 'true')
        
        # Serialize the data
        challenge_data = []
        for challenge in challenges:
            challenge_data.append({
                "id": challenge.id,
                "title": challenge.title,
                "description": challenge.description,
                "difficulty": challenge.difficulty,
                "category": challenge.category,
                "points": challenge.points,
                "is_active": challenge.is_active,
                "created_at": challenge.created_at.isoformat()
            })
        
        return Response({
            "count": len(challenge_data),
            "results": challenge_data
        })


class SkillListAPI(APIView):
    """
    API endpoint to list available skills for upskilling.
    """
    @swagger_auto_schema(
        operation_summary="List Available Skills",
        operation_description="Retrieve a list of all available skills for upskilling programs.",
        responses={
            200: openapi.Response(
                description="Skills retrieved successfully",
                examples={
                    "application/json": {
                        "count": 15,
                        "results": [
                            {
                                "id": 1,
                                "name": "Network Security",
                                "description": "Learn about network security fundamentals and best practices",
                                "slug": "network-security",
                                "created_at": "2024-01-01T00:00:00Z"
                            }
                        ]
                    }
                }
            ),
            401: 'Authentication required'
        },
        tags=["Skills"]
    )
    def get(self, request):
        skills = Skill.objects.all()
        
        skill_data = []
        for skill in skills:
            skill_data.append({
                "id": skill.id,
                "name": skill.name,
                "description": skill.description,
                "slug": skill.slug,
                "created_at": skill.created_at.isoformat() if hasattr(skill, 'created_at') else None
            })
        
        return Response({
            "count": len(skill_data),
            "results": skill_data
        })


class LeaderboardAPI(APIView):
    """
    API endpoint to retrieve leaderboard data.
    """
    @swagger_auto_schema(
        operation_summary="Get Leaderboard",
        operation_description="Retrieve leaderboard data for cybersecurity challenges with optional category filtering.",
        manual_parameters=[
            openapi.Parameter(
                'category',
                openapi.IN_QUERY,
                description="Filter by challenge category",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'limit',
                openapi.IN_QUERY,
                description="Number of top entries to return (default: 10)",
                type=openapi.TYPE_INTEGER
            )
        ],
        responses={
            200: openapi.Response(
                description="Leaderboard data retrieved successfully",
                examples={
                    "application/json": {
                        "category": "web_security",
                        "entries": [
                            {
                                "rank": 1,
                                "email": "john@example.com",
                                "first_name": "John",
                                "last_name": "Doe",
                                "total_points": 2500,
                                "completed_challenges": 15
                            }
                        ]
                    }
                }
            ),
            401: 'Authentication required'
        },
        tags=["Leaderboard"]
    )
    def get(self, request):
        category = request.query_params.get('category', '')
        limit = int(request.query_params.get('limit', 10))
        
        # Get leaderboard entries
        if category:
            entries = LeaderBoardTable.objects.filter(category=category).order_by('-total_points')[:limit]
        else:
            entries = LeaderBoardTable.objects.all().order_by('-total_points')[:limit]
        
        leaderboard_data = []
        for rank, entry in enumerate(entries, 1):
            leaderboard_data.append({
                "rank": rank,
                "email": entry.user.email,
                "first_name": entry.first_name,
                "last_name": entry.last_name,
                "total_points": entry.total_points,
                "category": entry.category
            })
        
        return Response({
            "category": category or "all",
            "entries": leaderboard_data
        })


class HealthCheckAPI(APIView):
    """
    API endpoint for health check and system status.
    """
    @swagger_auto_schema(
        operation_summary="Health Check",
        operation_description="Check the health status of the API and system components.",
        responses={
            200: openapi.Response(
                description="System is healthy",
                examples={
                    "application/json": {
                        "status": "healthy",
                        "timestamp": "2024-01-15T10:30:00Z",
                        "version": "1.0.0",
                        "database": "connected",
                        "services": {
                            "api": "operational",
                            "database": "operational",
                            "email": "operational"
                        }
                    }
                }
            ),
            503: 'Service unavailable'
        },
        tags=["System"]
    )
    def get(self, request):
        try:
            # Check database connection
            User.objects.count()
            db_status = "connected"
        except Exception:
            db_status = "disconnected"
        
        health_data = {
            "status": "healthy" if db_status == "connected" else "unhealthy",
            "timestamp": timezone.now().isoformat(),
            "version": "1.0.0",
            "database": db_status,
            "services": {
                "api": "operational",
                "database": "operational" if db_status == "connected" else "down",
                "email": "operational"
            }
        }
        
        status_code = 200 if db_status == "connected" else 503
        return Response(health_data, status=status_code)

def leaderboard(request):
    #Select category to display leaderboard table
    selected_category = request.GET.get('category', '')
    categories = LeaderBoardTable.objects.values_list('category', flat=True).distinct()
    if selected_category:
        leaderboard_entry = LeaderBoardTable.objects.filter(category=selected_category).order_by('-total_points')[:10]
    else:
        leaderboard_entry = LeaderBoardTable.objects.none()  # Show nothing by default

    context = {
        'entries': leaderboard_entry,
        'categories': categories,
        'selected_category': selected_category,

    }
    return render(request, 'pages/leaderboard.html', context)

def leaderboard_update():
    LeaderBoardTable.objects.all().delete()
    users = User.objects.all()
    for user in users:
        challenges_category = (UserChallenge.objects.filter(user=user, completed=True).values('category_challenges').annotate(total_points=Sum('score')))

        for categories in challenges_category:
            category = categories['category_challenges']
            total_points = categories['total_points'] or 0

            if total_points > 0:
                LeaderBoardTable.objects.create(first_name=user.first_name, last_name=user.last_name, category=category, total_points=total_points)



def cyber_quiz(request):
    """
    View for the cybersecurity quiz page.
    """
    return render(request, 'pages/challenges/quiz.html')


def comphrehensive_reports(request):
    reports = AppAttackReport.objects.all().order_by('-year')
    return render(request, 'pages/appattack/comprehensive_reports.html', {'reports': reports})

def pen_testing(request):
    if request.method == 'POST':
        form = PenTestingRequestForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Request submitted successfully.")
            return redirect('pen-testing')
    else:
        form = PenTestingRequestForm()
    return render(request, 'pages/appattack/pen_testing.html', {'form': form})

def secure_code_review(request):
    if request.method == 'POST':
        form = SecureCodeReviewRequestForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Request submitted successfully.")
            return redirect('secure-code-review')
    else:
        form = SecureCodeReviewRequestForm()
    return render(request, 'pages/appattack/secure_code_review.html', {'form': form})

@login_required
def pen_testing_form_view(request):
    if request.method == 'POST':
        form = PenTestingRequestForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Request submitted successfully!")
            return redirect('/appattack')
    else:
        form = PenTestingRequestForm()
    return render(request, 'pages/appattack/pen_testing_form.html', {'form': form, 'title': "Pen Testing Request"})

@login_required
def secure_code_review_form_view(request):
    if request.method == 'POST':
        form = SecureCodeReviewRequestForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Request submitted successfully!")
            return redirect('/appattack')
    else:
        form = SecureCodeReviewRequestForm()
    return render(request, 'pages/appattack/secure_code_review_form.html', {'form': form, 'title': "Secure Code Review Request"})


@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        logout(request)
        messages.success(request, "Your account has been deleted.")
        return redirect('login') 
    return HttpResponseNotAllowed(['POST'])

def tools_home(request):
    return render(request, 'pages/pt_gui/tools/index.html')

def aircrack_view(request):
    return render(request, 'pages/pt_gui/tools/aircrack/index.html')

def arjun_view(request):
    return render(request, 'pages/pt_gui/tools/arjun/index.html')

def rainbow_view(request):
    return render(request, 'pages/pt_gui/tools/rainbowcrack/index.html')

def airbase_view(request):
    return render(request, 'pages/pt_gui/tools/airbase/index.html')

def amap_view(request):
    return render(request, 'pages/pt_gui/tools/amap/index.html')

def amass_view(request):
    return render(request, 'pages/pt_gui/tools/amass/index.html')

def arpaname_view(request):
    return render(request, 'pages/pt_gui/tools/arpaname/index.html')

def policy_deployment(request):
    return render(request, 'pages/policy_deployment.html')
 #Health Check Function
def health_check(request):
    return JsonResponse({"status": "ok"}, status=200) 


# Challenge Management Views

class StaffRequiredMixin(UserPassesTestMixin):
    #Check if user is staff
    
    def test_func(self):
        return self.request.user.is_authenticated and (self.request.user.is_staff or self.request.user.is_superuser)
    
    def handle_no_permission(self):
        print(f"DEBUG: Access denied for user {self.request.user}")
        from django.shortcuts import redirect
        # Redirect to login page instead of raising 403
        return redirect('login')
    
class ChallengeManagementView(StaffRequiredMixin, ListView):
    model = CyberChallenge
    template_name = 'admin/challenges/challenge_management.html'
    context_object_name = 'challenges'
    
    
    def get_queryset(self):
        queryset = CyberChallenge.objects.all().order_by('-created_at')
        print(f"DEBUG: Found {queryset.count()} challenges in queryset")
        return queryset

class ChallengeCreateView(StaffRequiredMixin, CreateView):
    
    model = CyberChallenge
    form_class = ChallengeForm
    template_name = 'admin/challenges/add_challenge.html'
    success_url = reverse_lazy('challenge_management')
    
    def form_valid(self, form):
        messages.success(self.request, f'Challenge "{form.instance.title}" was created successfully!')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Create New Challenge'
        context['submit_text'] = 'Create Challenge'
        return context
    
class ChallengeUpdateView(StaffRequiredMixin, UpdateView):
  #edit challenge 
    model = CyberChallenge
    form_class = ChallengeForm
    template_name = 'admin/challenges/edit_challenge.html'
    success_url = reverse_lazy('challenge_management')
    
    def form_valid(self, form):
        messages.success(self.request, f'Challenge "{form.instance.title}" was updated successfully!')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = f'Edit Challenge: {self.object.title}'
        context['submit_text'] = 'Update Challenge'
        context['is_edit'] = True
        return context
class ChallengeDeleteView(StaffRequiredMixin, DeleteView):
    model = CyberChallenge
    template_name = 'admin/challenges/confirm_delete.html'
    success_url = reverse_lazy('challenge_management')
    
    def delete(self, request, *args, **kwargs):
        challenge = self.get_object()
        challenge_title = challenge.title
        response = super().delete(request, *args, **kwargs)
        messages.success(request, f'Challenge "{challenge_title}" was permanently deleted.')
        return response


class ChallengeArchiveView(StaffRequiredMixin, View):
    def get(self, request, pk):
        challenge = get_object_or_404(CyberChallenge, pk=pk)
        return render(request, 'admin/challenges/archive_challenge.html', {'object': challenge})

    def post(self, request, pk):
        challenge = get_object_or_404(CyberChallenge, pk=pk)
        
        # Handle JSON request body for AJAX
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            try:
                import json
                data = json.loads(request.body.decode('utf-8'))
                action = data.get('action', '')
                
                if action == 'archive':
                    challenge.is_active = False
                elif action == 'unarchive':
                    challenge.is_active = True
                else:
                    # Default toggle behavior
                    challenge.is_active = not challenge.is_active
            except (json.JSONDecodeError, KeyError):
                # Default toggle behavior if no valid JSON
                challenge.is_active = not challenge.is_active
        else:
            # Default toggle behavior for non-AJAX requests
            challenge.is_active = not challenge.is_active
            
        challenge.save()
        
        status = "archived" if not challenge.is_active else "unarchived"
        messages.success(request, f'Challenge "{challenge.title}" was {status} successfully!')
        
        # Return JSON response for AJAX requests
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'is_active': challenge.is_active,
                'message': f'Challenge "{challenge.title}" was {status} successfully!'
            })
        
        return redirect('challenge_management')


class ChallengePreviewView(StaffRequiredMixin, View):
    
    
    def _format_correct_answer(self, challenge):
        
        if not challenge.correct_answer:
            return None
            
        try:
           
            parsed = json.loads(challenge.correct_answer)
            if isinstance(parsed, list):
                return parsed
            return challenge.correct_answer
        except (json.JSONDecodeError, TypeError):
        
            return challenge.correct_answer
    
    def get(self, request, pk):
        challenge = get_object_or_404(CyberChallenge, pk=pk)
        
        choices_display = None
        if challenge.choices and challenge.challenge_type == 'mcq':
            if isinstance(challenge.choices, list):
                choices_display = challenge.choices
            else:
                try:
                    import json
                    choices_display = json.loads(challenge.choices)
                except (json.JSONDecodeError, TypeError):
                    choices_display = [challenge.choices]
        
        data = {
            'id': challenge.id,
            'title': challenge.title,
            'description': challenge.description,
            'question': challenge.question,
            'explanation': challenge.explanation,
            'difficulty': challenge.get_difficulty_display(),
            'category': challenge.get_category_display(),
            'points': challenge.points,
            'challenge_type': challenge.challenge_type,  
            'challenge_type_display': challenge.get_challenge_type_display(), 
            'time_limit': challenge.time_limit,
            'correct_answer': self._format_correct_answer(challenge),
            'choices': choices_display,
            'starter_code': challenge.starter_code,
            'sample_input': challenge.sample_input,
            'expected_output': challenge.expected_output,
            'is_active': challenge.is_active,
            'created_at': challenge.created_at.strftime('%B %d, %Y at %I:%M %p'),
            'updated_at': challenge.updated_at.strftime('%B %d, %Y at %I:%M %p'),
        }
        
        return JsonResponse(data)
class ResourceListView(ListView):
    template_name = "resources/list.html"
    model = Resource
    context_object_name = "resources"
    paginate_by = 12
    def get_queryset(self):
        qs = Resource.objects.filter(is_published=True)
        cat = self.request.GET.get("category")
        q = self.request.GET.get("q")
        if cat: qs = qs.filter(category=cat)
        if q:   qs = qs.filter(Q(title__icontains=q) | Q(summary__icontains=q))
        return qs

class ResourceDetailView(DetailView):
    template_name = "resources/detail.html"
    model = Resource
    slug_field = "slug"
    slug_url_kwarg = "slug"
    def get_queryset(self):
        return Resource.objects.filter(is_published=True)

def resource_download(request, pk: int):
    obj = get_object_or_404(Resource, pk=pk, is_published=True)
    if not obj.file:
        raise Http404("No file attached.")

    ext = Path(obj.file.name).suffix or ""
    filename = f"{slugify(obj.title)}{ext}"

    ctype, _ = mimetypes.guess_type(obj.file.name)
    resp = FileResponse(
        obj.file.open("rb"),
        as_attachment=True,
        filename=filename,
        content_type=ctype or "application/octet-stream",
    )
    # size helps some downloaders
    try:
        resp["Content-Length"] = obj.file.size
    except Exception:
        pass


    resp["X-Content-Type-Options"] = "nosniff"
    return resp

def tip_today(request):
    texts = list(Tip.objects.filter(is_active=True).values_list("text", flat=True))
    if not texts:
        return JsonResponse({"tip": "Stay safe online!"})

    state, _ = TipRotationState.objects.get_or_create(lock="default")

    now = timezone.now()
    needs_rotate = (
        state.rotated_at is None
        or (now - state.rotated_at) >= timedelta(hours=24)
        or state.last_index >= len(texts)  # handle when you add/remove tips
        or state.last_index < -1
    )

    if needs_rotate:
        state.last_index = (state.last_index + 1) % len(texts)
        state.rotated_at = now
        state.save(update_fields=["last_index", "rotated_at"])

    return JsonResponse({"tip": texts[state.last_index]})


@login_required
def vault_view(request):
    """View for the document vault"""
    documents = VaultDocument.objects.all()
    
    # Handle filtering
    type_filter = request.GET.get('type', '')
    if type_filter:
        if type_filter == 'pdf':
            documents = documents.filter(content_type__icontains='pdf')
        elif type_filter == 'word':
            documents = documents.filter(content_type__icontains='word')
        elif type_filter == 'excel':
            documents = documents.filter(content_type__icontains='excel')
        elif type_filter == 'powerpoint':
            documents = documents.filter(content_type__icontains='powerpoint')
        elif type_filter == 'image':
            documents = documents.filter(content_type__icontains='image')
    
    # Handle file upload
    if request.method == 'POST':
        form = VaultUploadForm(request.POST, request.FILES)
        if form.is_valid():
            vault_doc = form.save(commit=False)
            vault_doc.uploaded_by = request.user
            vault_doc.original_name = request.FILES['file'].name
            vault_doc.content_type = request.FILES['file'].content_type
            vault_doc.size_bytes = request.FILES['file'].size
            vault_doc.save()
            form.save_m2m()  # Save many-to-many relationships
            return redirect('vault')
    else:
        form = VaultUploadForm()
    
    context = {
        'documents': documents,
        'form': form,
        'type_filter': type_filter,
    }
    return render(request, 'pages/vault.html', context)

def delete_document(request, doc_id):
    doc = get_object_or_404(VaultDocument, id=doc_id)

    # Only staff or the uploader can delete
    if not (request.user.is_staff or doc.uploaded_by_id == request.user.id):
        raise PermissionDenied("You don't have permission to delete this document.")

    if request.method == "POST":
        # optionally remove the file from storage too
        if doc.file:
            doc.file.delete(save=False)
        doc.delete()
        return redirect('vault')

    # if someone hits the URL with GET, just go back
    return redirect('vault')


def debug_auth_status(request):
    """
    Debug view to check authentication status
    """
    debug_info = {
        'user_authenticated': request.user.is_authenticated,
        'user_email': request.user.email if request.user.is_authenticated else 'Not authenticated',
        'session_keys': list(request.session.keys()),
        'session_data': {
            'oauth_authenticated': request.session.get('oauth_authenticated', False),
            'microsoft_oauth_success': request.session.get('microsoft_oauth_success', False),
            'user_authenticated': request.session.get('user_authenticated', False),
            'force_dashboard_redirect': request.session.get('force_dashboard_redirect', False),
            'bypass_login_redirect': request.session.get('bypass_login_redirect', False),
        },
        'current_path': request.path,
        'full_path': request.get_full_path(),
    }
    
    from django.http import JsonResponse
    return JsonResponse(debug_info)


def test_login(request):
    """
    Test view to manually log in a user for testing
    """
    from django.contrib.auth import login, get_user_model
    from django.http import HttpResponseRedirect
    
    User = get_user_model()
    
    # Create or get a test user
    user, created = User.objects.get_or_create(
        username='test@deakin.edu.au',
        defaults={
            'email': 'test@deakin.edu.au',
            'first_name': 'Test',
            'last_name': 'User',
            'is_active': True,
        }
    )
    
    # Log in the user
    login(request, user)
    
    print(f"DEBUG: Test user logged in: {user.email}")
    print(f"DEBUG: User authenticated: {request.user.is_authenticated}")
    
    # Redirect to dashboard
    return HttpResponseRedirect('/dashboard/')

