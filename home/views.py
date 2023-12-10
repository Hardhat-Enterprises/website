from django.shortcuts import render
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetView, PasswordResetConfirmView
from .forms import RegistrationForm, UserLoginForm, UserPasswordResetForm, UserPasswordChangeForm, UserSetPasswordForm
from django.contrib.auth import logout
from django.shortcuts import render, redirect

# Create your views here.


def index(request):
    # Page from the theme
    return render(request, 'pages/index.html')

def abouts_us(request):
  return render(request, 'pages/about.html')

def appattack(request):
    return render(request, 'pages/appattack/main.html')


def products_services(request):
    # Page from the theme
    return render(request, 'pages/malware_visualization/products_and_services.html')


def malwarehome(request):

    # Page from the theme
    return render(request, 'pages/malware_visualization/main.html')


def malware_joinus(request):

    # Page from the theme
    return render(request, 'pages/malware_visualization/malware_viz_joinus.html')


def ptguihome(request):

    # Page from the theme
    return render(request, 'pages/pt_gui/main.html')

def ptgui_contact_us(request):
    return render(request, 'pages/pt_gui/contact-us.html')


def http_503(request):
    return render(request, 'pages/503.html')



# Authentication
class UserLoginView(LoginView):
  template_name = 'accounts/sign-in.html'
  form_class = UserLoginForm

def logout_view(request):
  logout(request)
  return redirect('/accounts/login')

def register(request):
  print("in register view")
  if request.method == 'POST':
    form = RegistrationForm(request.POST)
    if form.is_valid():
      form.save()
      print("Account created successfully!")
      return redirect('/accounts/login')
    else:
      print("Registration failed!")
  else:
    form = RegistrationForm()

  context = { 'form': form }
  return render(request, 'accounts/sign-up.html', context)

class UserPasswordResetView(PasswordResetView):
  template_name = 'accounts/password_reset.html'
  form_class = UserPasswordResetForm

class UserPasswordResetConfirmView(PasswordResetConfirmView):
  template_name = 'accounts/password_reset_confirm.html'
  form_class = UserSetPasswordForm

class UserPasswordChangeView(PasswordChangeView):
  template_name = 'accounts/password_change.html'
  form_class = UserPasswordChangeForm
def login_view(request):
    return render(request, 'pages/login.html')

def resources_view(request):
    return render(request, 'pages/resources.html.')
    
