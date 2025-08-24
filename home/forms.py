from django import forms
from django.forms import ModelForm
import re
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm, UsernameField
from django.contrib.auth import get_user_model
from captcha.fields import CaptchaField
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils.timezone import now
from datetime import timedelta
import logging
import re
import nh3

from .models import Student, Smishingdetection_join_us, Projects_join_us, Webpage, Project, Profile, Experience,UserBlogPage, SecurityEvent, JobApplication, CyberChallenge
from .models import PenTestingRequest, SecureCodeReviewRequest
from .validators import xss_detection
import json
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
    # ...........................................................

    # Newly added...........................
    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip()  # Normalize email
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
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'First Name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Last Name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'example@deakin.edu.au'
            })
        }



    # .......................................

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
    # ...........................................................

    # Newly added...........................
    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Define the regex pattern for the required email format
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        if not re.match(pattern, email):
            raise ValidationError(_("Email must be valid email."))
        
        return email
    # .......................................

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
            raise ValidationError(
                _("Too many login attempts. Please try again later."),
                code='too_many_attempts',
            )
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
            raise ValidationError(
            _("Too many login attempts. Please try again later."),
            code='too_many_attempts',
            )

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
    username = UsernameField(label='Client Email Address',widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "example@gmail.com"}))
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
    
    class Meta:
        model = Student
        fields = ("id", "year", "trimester", "unit", "course", "p1", "p2", "p3", )
        labels = {
            'p1': '1st Priority',
            'p2': '2nd Priority',
            'p3': '3rd Priority',
        }

class sd_JoinUsForm(forms.ModelForm):
    class Meta:
        model = Smishingdetection_join_us
        fields = ['name', 'email', 'message']


class projects_JoinUsForm(forms.ModelForm):
    class Meta:
        model = Projects_join_us
        fields = ['name', 'email', 'message','page_name']
    
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
        choices=[
            ('Excellent', 'Excellent'),
            ('Good', 'Good'),
            ('Poor', 'Poor'),
            ('Disappointing', 'Disappointing')
        ],
        required=True,
        label='Rating'
    )
User = get_user_model()

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'First Name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Last Name'
            }),
        }

class ProfileUpdateForm(forms.ModelForm):  
    class Meta:
        model = Profile
        fields = ['avatar', 'bio', 'linkedin', 'github', 'location']
        widgets = {
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Tell us about yourself'
            }),
            'linkedin': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'LinkedIn Profile URL'
            }),
            'github': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'GitHub Profile URL'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'City, Country'
            })
        }

class CaptchaForm(forms.Form):
    captcha = CaptchaField()
        


class UserBlogPageForm(ModelForm):
    file = forms.FileField(required=False)

    class Meta:
        model = UserBlogPage
        fields = ['name', 'title', 'description', 'file']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your name'}),
            'title': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Your title', 'rows': 2}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Your description'}),
        }

#Newly Added
class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)

    def clean_name(self):
        name = self.cleaned_data['name']
        name = xss_detection(name)
        return nh3.clean(name, tags=set(), attributes={}, link_rel=None)

    def clean_message(self):
        message = self.cleaned_data['message']
        message = xss_detection(message)
        return nh3.clean(message, tags=set(), attributes={}, link_rel=None)
        
# Experience Form
class ExperienceForm(forms.ModelForm):
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


# class JobApplicationForm(forms.ModelForm):
    
#     class Meta:
#         model = JobApplication
#         fields = ['name', 'email', 'resume', 'cover_letter']
    
class JobApplicationForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}))
    resume = forms.FileField(widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))

    cover_letter = forms.FileField(widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))

class PenTestingRequestForm(forms.ModelForm):
    terms_agreed = forms.BooleanField(required=True, label="I agree to the terms and conditions")

    class Meta:
        model = PenTestingRequest
        fields = ['name', 'email', 'github_repo_link', 'terms_agreed']

class SecureCodeReviewRequestForm(forms.ModelForm):
    terms_agreed = forms.BooleanField(required=True, label="I agree to the terms and conditions")

    class Meta:
        model = SecureCodeReviewRequest
        fields = ['name', 'email', 'github_repo_link', 'terms_agreed']

# Cyber Challenge Forms ------------------------------------------------------------

class ChallengeForm(forms.ModelForm):
    choices_text = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Enter choices separated by newlines', 'class': 'form-control'}), required=False, help_text="for Multiple Choice Questions, Enter each choice per line"
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
        
        print(f"DEBUG: clean_correct_answer called")
        print(f"DEBUG: challenge_type = {challenge_type}")
        print(f"DEBUG: correct_answer (before processing) = {repr(correct_answer)}")
        
        if not correct_answer:
            raise forms.ValidationError("Correct answer is required.")
        
        # Only MCQ challenges need JSON array format
        if challenge_type == 'mcq':
            try:
                # Try to parse as JSON
                parsed = json.loads(correct_answer)
                if not isinstance(parsed, list):
                    # If it's not a list, convert single answer to list format
                    result = json.dumps([correct_answer])
                    print(f"DEBUG: MCQ - converted to JSON array: {result}")
                    return result
                # check list not empty
                if not parsed:
                    raise forms.ValidationError("At least one correct answer is required.")
                print(f"DEBUG: MCQ - already JSON array: {correct_answer}")
                return correct_answer
            except json.JSONDecodeError:
                # If not json treat as single answer and convert to json list
                result = json.dumps([correct_answer])
                print(f"DEBUG: MCQ - JSON decode error, converted to array: {result}")
                return result
        
        # For fix_code challenges, return the answer without JSON wrapping
        print(f"DEBUG: fix_code - returning as-is: {repr(correct_answer)}")
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