from django import forms
from django.core.validators import RegexValidator
from django.contrib.auth.models import Group
from django.forms import ModelForm
import re
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm, UsernameField
from django.contrib.auth import get_user_model
from captcha.fields import CaptchaField
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.utils.timezone import now
from datetime import timedelta
from .models import VaultDocument
import logging
import nh3

from .models import Student, Smishingdetection_join_us, Projects_join_us, Webpage, Project, Profile, Experience, UserBlogPage, SecurityEvent, JobApplication, CyberChallenge
from .models import PenTestingRequest, SecureCodeReviewRequest
from .validators import xss_detection
from utils.sanitizer import clean_text, clean_email, clean_url, clean_html, clean_numeric
import json
from .models import VaultDocument, CyberChallenge

logger = logging.getLogger(__name__)
User = get_user_model()


def possible_years(first_year_in_scroll, last_year_in_scroll):
    p_year = []
    for i in range(first_year_in_scroll, last_year_in_scroll, -1):
        p_year_tuple = str(i), i
        p_year.append(p_year_tuple)
    return p_year


class RegistrationForm(UserCreationForm):
    # Newly added...........................
    email = forms.EmailField(
        label=_("Email"),
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
    )
    # .......................................

    password1 = forms.CharField(
        label=_("Your Password"),
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
    )
    password2 = forms.CharField(
        label=_("Confirm Password"),
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}),
    )
    # Newly added................................................
    def clean_password1(self):
        password = self.cleaned_data.get('password1')

        # Check individual requirements - this matches the frontend validation
        if len(password) < 8:
            raise ValidationError(_("Password must be at least 8 characters long."))

        if not re.search(r'[a-z]', password):
            raise ValidationError(_("Password must include at least one lowercase letter."))

        if not re.search(r'[A-Z]', password):
            raise ValidationError(_("Password must include at least one uppercase letter."))

        if not re.search(r'\d', password):
            raise ValidationError(_("Password must include at least one number."))

        if not re.search(r'[@$!%*?&]', password):
            raise ValidationError(_("Password must include at least one special character (@, $, !, %, *, ?, &)."))

        return password
    # .........................................................

    # Keep strict Deakin email validation with debug logs
    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip()
        print(f"Validating email: {email}")  # Debugging log

        # Regex pattern for validating Deakin email addresses
        pattern = r'^[a-zA-Z0-9._%+-]+@([a-zA-Z0-9-]+\.)?deakin\.edu\.au$'

        if not re.match(pattern, email):
            print(f"Validation failed for email: {email}")  # Debug log for failed validation
            raise ValidationError(_("Email must match your Deakin email."))

        print(f"Validation succeeded for email: {email}")  # Debug log for success
        return email

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', )
        labels = {
            'first_name': _('First Name'),
            'last_name': _('Last Name'),
            'email': _('Deakin Email Address'),
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'example@deakin.edu.au'})
        }

    def save(self, commit=True):
        """
        Overrides the save method to ensure the user instance is saved correctly.
        """
        user = super().save(commit=False)
        if commit:
            user.save()
        return user


class ClientRegistrationForm(UserCreationForm):
    # Newly added...........................
    email = forms.EmailField(
        label=_("Business Email"),
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
    )
    # .......................................

    business_name = forms.CharField(
        label=_("Business Name"),
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Business Name'}),
    )

    password1 = forms.CharField(
        label=_("Your Password"),
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
    )
    password2 = forms.CharField(
        label=_("Confirm Password"),
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}),
    )
    # Newly added................................................
    def clean_password1(self):
        password = self.cleaned_data.get('password1')

        # Check individual requirements - this matches the frontend validation
        if len(password) < 8:
            raise ValidationError(_("Password must be at least 8 characters long."))

        if not re.search(r'[a-z]', password):
            raise ValidationError(_("Password must include at least one lowercase letter."))

        if not re.search(r'[A-Z]', password):
            raise ValidationError(_("Password must include at least one uppercase letter."))

        if not re.search(r'\d', password):
            raise ValidationError(_("Password must include at least one number."))

        if not re.search(r'[@$!%*?&]', password):
            raise ValidationError(_("Password must include at least one special character (@, $, !, %, *, ?, &)."))

        return password
    # .........................................................

    # Sanitized general email (business)
    def clean_email(self):
        return clean_email(self.cleaned_data.get('email', ''))

    def clean_business_name(self):
        return clean_text(self.cleaned_data.get('business_name', ''))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', )
        labels = {
            'first_name': _('First Name'),
            'last_name': _('Last Name'),
            'email': _('Business Email Address'),
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'example@business.com'})
        }


class UserLoginForm(AuthenticationForm):
    username = UsernameField(
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "example@deakin.edu.au"})
    )
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Password"}),
    )

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        self.request = request

    def confirm_login_allowed(self, user):
        failure_count_time = timezone.now() - timedelta(minutes=15)
        login_failures_count = SecurityEvent.objects.filter(
            event_type='login_failure',
            timestamp__gte=failure_count_time
        ).count()

        if login_failures_count > 2:
            raise ValidationError(_("Too many login attempts. Please try again later."), code='too_many_attempts')
        else:
            super().confirm_login_allowed(user)

            # Log successful login event
            ip_address = self.request.META.get('REMOTE_ADDR') if self.request else 'Unknown IP'
            SecurityEvent.objects.create(
                user=user,
                event_type='login_success',
                ip_address=ip_address,
                details='User logged in successfully.'
            )
            print(f'User {user} logged in successfully.')

    def get_invalid_login_error(self):
        # Log failed login event
        faliure_count_time = timezone.now() - timedelta(minutes=15)
        login_failures_count = SecurityEvent.objects.filter(
            event_type='login_failure',
            timestamp__gte=faliure_count_time
        ).count()

        if login_failures_count > 2:
            raise ValidationError(_("Too many login attempts. Please try again later."), code='too_many_attempts')

        ip_address = self.request.META.get('REMOTE_ADDR') if self.request else 'Unknown IP'
        SecurityEvent.objects.create(
            user=None,  # No user as login failed
            event_type='login_failure',
            ip_address=ip_address,
            details=f'Failed login attempt for username: {self.cleaned_data.get("username", "Unknown")}'
        )
        print(f'Failed login attempt for username: {self.cleaned_data.get("username", "Unknown")}')
        return super().get_invalid_login_error()


class ClientLoginForm(AuthenticationForm):
    username = UsernameField(label='Client Email Address',
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "example@gmail.com"}))
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Password"}),
    )

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        self.request = request

    def confirm_login_allowed(self, user):
        super().confirm_login_allowed(user)
        # Log successful login event
        ip_address = self.request.META.get('REMOTE_ADDR') if self.request else 'Unknown IP'
        SecurityEvent.objects.create(
            user=user,
            event_type='login_success',
            ip_address=ip_address,
            details='User logged in successfully.'
        )
        print(f'User {user} logged in successfully.')

    def get_invalid_login_error(self):
        # Log failed login event
        ip_address = self.request.META.get('REMOTE_ADDR') if self.request else 'Unknown IP'
        SecurityEvent.objects.create(
            user=None,  # No user as login failed
            event_type='login_failure',
            ip_address=ip_address,
            details=f'Failed login attempt for username: {self.cleaned_data.get("username", "Unknown")}'
        )
        print(f'Failed login attempt for username: {self.cleaned_data.get("username", "Unknown")}')
        return super().get_invalid_login_error()


class UserPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'example@deakin.edu.au'
    }), label=_("Your Email"))


class UserSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'New Password'
    }), label=_("New Password"))
    new_password2 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Confirm New Password'
    }), label=_("Confirm New Password"))


class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Old Password'
    }), label=_("Old Password"))
    new_password1 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'New Password'
    }), label=_("New Password"))
    new_password2 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Confirm New Password'
    }), label=_("Confirm New Password"))

class StudentForm(forms.ModelForm):
    id = forms.IntegerField(label=_('Deakin Student ID'))
    year = forms.ChoiceField(
        choices=possible_years(((timezone.now()).year), 2020),
        label=_("Year")
    )

    def clean_id(self):
        return clean_numeric(self.cleaned_data.get('id'))

    class Meta:
        model = Student
        fields = ("id", "year", "trimester", "unit", "course", "p1", "p2", "p3", )
        labels = {
            'p1': '1st Priority',
            'p2': '2nd Priority',
            'p3': '3rd Priority',
        }


class sd_JoinUsForm(forms.ModelForm):
    def clean_name(self):
        return clean_text(self.cleaned_data.get('name', ''))

    def clean_email(self):
        return clean_email(self.cleaned_data.get('email', ''))

    def clean_message(self):
        return clean_text(self.cleaned_data.get('message', ''))

    class Meta:
        model = Smishingdetection_join_us
        fields = ['name', 'email', 'message']


class projects_JoinUsForm(forms.ModelForm):
    def clean_name(self):
        return clean_text(self.cleaned_data.get('name', ''))

    def clean_email(self):
        return clean_email(self.cleaned_data.get('email', ''))

    def clean_message(self):
        return clean_text(self.cleaned_data.get('message', ''))

    def clean_page_name(self):
        return clean_text(self.cleaned_data.get('page_name', ''))

    class Meta:
        model = Projects_join_us
        fields = ['name', 'email', 'message', 'page_name']


class Upskilling_JoinProjectForm(forms.ModelForm):
    p1 = forms.ModelChoiceField(queryset=Project.objects.all(), required=True)
    p2 = forms.ModelChoiceField(queryset=Project.objects.all(), required=True)
    p3 = forms.ModelChoiceField(queryset=Project.objects.all(), required=True)

    class Meta:
        model = Student
        fields = ['year', 'trimester', 'unit', 'course', 'p1', 'p2', 'p3']
        widgets = {
            'trimester': forms.Select(choices=Student.TRIMESTERS),
            'unit': forms.Select(choices=Student.UNITS),
            'course': forms.Select(choices=Student.COURSES),
        }

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('p1')
        p2 = cleaned_data.get('p2')
        p3 = cleaned_data.get('p3')

        if p1 and p2 and p3:
            if len({p1, p2, p3}) < 3:
                self.add_error(None, 'Project preferences must be unique.')


class NewWebURL(forms.ModelForm):
    def clean_url(self):
        return clean_url(self.cleaned_data.get('url', ''))

    def clean_title(self):
        return clean_text(self.cleaned_data.get('title', ''))

    class Meta:
        model = Webpage
        fields = ['id', 'url', 'title']


class FeedbackForm(forms.Form):
    name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'style': 'width: 100%;',
            'placeholder': 'Your Name'
        }),
        max_length=100,
        required=True,
        label='Name'
    )
    feedback = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'style': 'width: 100%; height: 200px;',
            'placeholder': 'Share your feedback here...'
        }),
        required=True,
        label='Customer Feedback'
    )
    rating = forms.ChoiceField(
        choices=[('Excellent', 'Excellent'), ('Good', 'Good'), ('Poor', 'Poor'), ('Disappointing', 'Disappointing')],
        required=True,
        label='Rating'
    )

    def clean_name(self):
        return clean_text(self.cleaned_data.get('name', ''))

    def clean_feedback(self):
        return clean_text(self.cleaned_data.get('feedback', ''))


class UserUpdateForm(forms.ModelForm):
    def clean_first_name(self):
        return clean_text(self.cleaned_data.get('first_name', ''))

    def clean_last_name(self):
        return clean_text(self.cleaned_data.get('last_name', ''))

    class Meta:
        model = User
        fields = ['first_name', 'last_name']
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
        }

# Strict LinkedIn personal profile: https://www.linkedin.com/in/<slug>[/]
linkedin_validator = RegexValidator(
    regex=r"^https:\/\/(www\.)?linkedin\.com\/in\/[A-Za-z0-9\-_%]+\/?$",
    message="Enter a valid LinkedIn personal profile URL (e.g., https://www.linkedin.com/in/your-handle).",
    flags=re.IGNORECASE,
)

# GitHub username rules: 1–39 chars, alnum or hyphen, cannot start/end with hyphen
# URL form: https://github.com/<username>[/]
github_validator = RegexValidator(
    regex=r"^https:\/\/(www\.)?github\.com\/([a-z\d](?:[a-z\d]|-(?=[a-z\d])){0,38})\/?$",
    message="Enter a valid GitHub profile URL (e.g., https://github.com/username).",
    flags=re.IGNORECASE,
)

class ProfileUpdateForm(forms.ModelForm):
    # Override model fields so we can attach validators + widgets
    linkedin = forms.URLField(
        required=False,
        validators=[linkedin_validator],
        widget=forms.URLInput(attrs={
            'class': 'form-control',
            'placeholder': 'LinkedIn Profile URL',
            'pattern': r'https://(www\.)?linkedin\.com/in/[A-Za-z0-9\-_%]+/?',
            'title': 'e.g., https://www.linkedin.com/in/your-handle'
        })
    )

    github = forms.URLField(
        required=False,
        validators=[github_validator],
        widget=forms.URLInput(attrs={
            'class': 'form-control',
            'placeholder': 'GitHub Profile URL',
            'pattern': r'https://(www\.)?github\.com/([a-z\d](?:[a-z\d]|-(?=[a-z\d])){0,38})/?',
            'title': 'e.g., https://github.com/yourname'
        })
    )

    class Meta:
        model = Profile
        fields = ['avatar', 'bio', 'linkedin', 'github', 'location']
        widgets = {
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Tell us about yourself'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'City, Country'
            }),
        }


class CaptchaForm(forms.Form):
    captcha = CaptchaField()


class UserBlogPageForm(ModelForm):
    def clean_name(self):
        return clean_text(self.cleaned_data.get('name', ''))

    def clean_title(self):
        return clean_text(self.cleaned_data.get('title', ''))

    def clean_description(self):
        return clean_html(self.cleaned_data.get('description', ''))

    class Meta:
        model = UserBlogPage
        fields = ['name', 'title', 'description', 'file']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Your name')}),
            'title': forms.Textarea(attrs={'class': 'form-control', 'placeholder': _('Your title'), 'rows': 2}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': _('Your description')}),
        }


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)

    def clean_name(self):
        return clean_text(self.cleaned_data.get('name', ''))

    def clean_message(self):
        return clean_text(self.cleaned_data.get('message', ''))


class ExperienceForm(forms.ModelForm):
    def clean_name(self):
        return clean_text(self.cleaned_data.get('name', ''))

    def clean_feedback(self):
        return clean_text(self.cleaned_data.get('feedback', ''))

    class Meta:
        model = Experience
        fields = ['name', 'feedback']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your name'}),
            'feedback': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Your feedback'}),
        }

    def __init__(self, *args, **kwargs):
        super(ExperienceForm, self).__init__(*args, **kwargs)
        self.fields['name'].required = False  # Let us handle this manually in clean()

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        anonymous = self.data.get('anonymous')  # Read from raw POST data (checkbox input)
        if not anonymous and not name:
            self.add_error('name', 'Please enter your name or check "Make it anonymous".')


class JobApplicationForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}))
    resume = forms.FileField(widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))
    cover_letter = forms.FileField(widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))

    def clean_name(self):
        return clean_text(self.cleaned_data.get('name', ''))

    def clean_email(self):
        return clean_email(self.cleaned_data.get('email', ''))


class PenTestingRequestForm(forms.ModelForm):
    terms_accepted = forms.BooleanField(required=True, label="I agree to the terms and conditions")

    def clean_name(self):
        return clean_text(self.cleaned_data.get('name', ''))

    def clean_email(self):
        return clean_email(self.cleaned_data.get('email', ''))

    def clean_github_repo_link(self):
        return clean_url(self.cleaned_data.get('github_repo_link', ''))

    class Meta:
        model = PenTestingRequest
        fields = ['name', 'email', 'github_repo_link', 'terms_accepted']


class SecureCodeReviewRequestForm(forms.ModelForm):
    terms_accepted = forms.BooleanField(required=True, label="I agree to the terms and conditions")

    def clean_name(self):
        return clean_text(self.cleaned_data.get('name', ''))

    def clean_email(self):
        return clean_email(self.cleaned_data.get('email', ''))

    def clean_github_repo_link(self):
        return clean_url(self.cleaned_data.get('github_repo_link', ''))

    class Meta:
        model = SecureCodeReviewRequest
        fields = ['name', 'email', 'github_repo_link', 'terms_accepted']

# Cyber Challenge Forms ------------------------------------------------------------

class ChallengeForm(forms.ModelForm):
    choices_text = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 3,
            'placeholder': 'Enter choices separated by newlines',
            'class': 'form-control'
        }),
        required=False,
        help_text="for Multiple Choice Questions, Enter each choice per line"
    )

    class Meta:
        model = CyberChallenge
        fields = [
            'title', 'description', 'question', 'explanation',
            'difficulty', 'category', 'points', 'challenge_type',
            'time_limit', 'correct_answer', 'starter_code',
            'sample_input', 'expected_output'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ' Enter challenge title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'brief description of the challenge'}),
            'question': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Enter the challenge question'}),
            'explanation': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Explanation for the correct answer'}),
            'difficulty': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'points': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 100}),
            'challenge_type': forms.Select(attrs={'class': 'form-control', 'id': 'challenge-type-select'}),
            'time_limit': forms.NumberInput(attrs={'class': 'form-control', 'min': 30, 'max': 333600, 'placeholder': 'Time in seconds'}),
            'correct_answer': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Enter the full correct code, not just what user inputs to fix'}),
            'starter_code': forms.Textarea(attrs={'class': 'form-control', 'rows': 8, 'placeholder': 'def solution():\n    # Your code here\n    pass'}),
            'sample_input': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Sample input for code challenges'}),
            'expected_output': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter Complete Expected Output'}),
        }
        labels = {
            'title': 'Challenge Title',
            'description': 'Description',
            'question': 'Question/Problem Statement',
            'explanation': 'Explanation',
            'difficulty': 'Difficulty Level',
            'category': 'Category',
            'points': 'Points',
            'challenge_type': 'Challenge Type',
            'time_limit': 'Time Limit (seconds)',
            'correct_answer': 'Correct Answer',
            'starter_code': 'Starter Code (for Fix the Code challenges)',
            'sample_input': 'Sample Input into code before running',
            'expected_output': 'Expected Output of code after running',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # If editing an existing challenge, populate choices_text
        if self.instance and self.instance.pk and self.instance.choices:
            if isinstance(self.instance.choices, list):
                self.fields['choices_text'].initial = '\n'.join(self.instance.choices)
            elif isinstance(self.instance.choices, str):
                try:
                    choices_list = json.loads(self.instance.choices)
                    self.fields['choices_text'].initial = '\n'.join(choices_list)
                except (json.JSONDecodeError, TypeError):
                    self.fields['choices_text'].initial = self.instance.choices

    def clean_choices_text(self):
        choices_text = self.cleaned_data.get('choices_text', '').strip()
        challenge_type = self.cleaned_data.get('challenge_type')

        if challenge_type == 'mcq' and not choices_text:
            raise forms.ValidationError("Choices are required for Multiple Choice questions.")

        return choices_text

    def clean_correct_answer(self):
        correct_answer = self.cleaned_data.get('correct_answer', '').strip()
        challenge_type = self.cleaned_data.get('challenge_type')

        if not correct_answer:
            raise forms.ValidationError("Correct answer is required.")

        # Only MCQ challenges need JSON array format
        if challenge_type == 'mcq':
            try:
                # Try to parse as JSON
                parsed = json.loads(correct_answer)
                if not isinstance(parsed, list):
                    # If it's not a list, convert single answer to list format
                    return json.dumps([correct_answer])
                # check list not empty
                if not parsed:
                    raise forms.ValidationError("At least one correct answer is required.")
                return correct_answer
            except json.JSONDecodeError:
                # If not json treat as single answer and convert to json list
                return json.dumps([correct_answer])

        # For fix_code challenges, return the answer without JSON wrapping
        return correct_answer

    def clean_starter_code(self):
        starter_code = self.cleaned_data.get('starter_code', '').strip()
        challenge_type = self.cleaned_data.get('challenge_type')

        if challenge_type == 'fix_code' and not starter_code:
            raise forms.ValidationError("Starter code is required for Fix the Code challenges.")

        return starter_code

    def save(self, commit=True):
        instance = super().save(commit=False)

        # Convert choices_text to JSON for multiple choice questions
        choices_text = self.cleaned_data.get('choices_text', '').strip()
        if choices_text and instance.challenge_type == 'mcq':
            choices_list = [choice.strip() for choice in choices_text.split('\n') if choice.strip()]
            instance.choices = choices_list
        else:
            instance.choices = None

        if commit:
            instance.save()
        return instance


class VaultUploadForm(forms.ModelForm):
    class Meta:
        model = VaultDocument
        fields = ['file', 'description', 'visibility', 'allowed_teams']  # NEW
        widgets = {
            'description': forms.TextInput(attrs={'placeholder': 'Optional description', 'class':'form-control'}),
            'visibility': forms.Select(attrs={'class': 'form-select'}),  # NEW
            'allowed_teams': forms.SelectMultiple(attrs={'class': 'form-select', 'size': '6'}),  # NEW
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # List all groups (teams). You can restrict to certain names if you wish.
        self.fields['allowed_teams'].queryset = Group.objects.all().order_by('name')

    def clean(self):
        cleaned = super().clean()
        vis = cleaned.get('visibility')
        teams = cleaned.get('allowed_teams')
        if vis == VaultDocument.VIS_TEAMS and (not teams or teams.count() == 0):
            raise forms.ValidationError("Select at least one team for 'Selected teams' visibility.")
        return cleaned
