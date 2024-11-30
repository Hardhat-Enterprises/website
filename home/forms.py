from django import forms
import re
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm, UsernameField
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from .models import Student, Smishingdetection_join_us, Projects_join_us, Webpage, Project, Profile
from django.contrib.auth.hashers import make_password

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
        # Define the regex pattern for the required password format
        pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
        
        if not re.match(pattern, password):
            raise ValidationError(
                _("Password must be at least 8 characters long and include uppercase, lawercase letters, numbers and special characters.")
            )
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
    # .......................................

    def set_password(self, raw_password):
        """
        Hashes the password using Django's password hashing system and returns it.
        """
        return make_password(raw_password)

    def save(self, commit=True):
        """
        Overrides the save method to hash the password before saving the user instance.
        """
        user = super().save(commit=False)
        raw_password = self.cleaned_data.get('password1')
        user.password = self.set_password(raw_password)
        if commit:
            user.save()
        return user

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

class UserLoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "example@deakin.edu.au"}))
    password = forms.CharField(
            label=_("Password"),
            strip=False,
            widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Password"}),
        )   

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
    name = forms.CharField(max_length=100, required=True, label='Name')
    feedback = forms.CharField(widget=forms.Textarea, required=True, label='Customer Feedback')
    rating = forms.ChoiceField(choices=[
        ('Excellent', 'Excellent'),
        ('Good', 'Good'),
        ('Poor', 'Poor'),
        ('Disappointing', 'Disappointing')
    ], required=True, label='Rating')
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
        fields = ['avatar', 'bio']
