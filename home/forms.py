from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm, UsernameField
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


from .models import Student, Smishingdetection_join_us, Projects_join_us, Webpage



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
        email = self.cleaned_data.get('email')
        # Define the regex pattern for the required email format
        pattern = r'^s\d{9}@deakin\.edu\.au$'
        
        if not re.match(pattern, email):
            raise ValidationError(_("Email must be match with your Deakin email."))
        
        return email
    # .......................................


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
        


class NewWebURL(forms.ModelForm):
    class Meta:
        model = Webpage
        fields = ['id', 'url', 'title']
            

