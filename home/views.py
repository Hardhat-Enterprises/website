from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetView, PasswordResetConfirmView
from django.contrib.auth import logout
from django.db.models import Count, F, Sum, Avg
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages

from utils.charts import generate_color_palette, colorPrimary, colorSuccess, colorDanger
from .models import Student, Project, Contact
from .forms import RegistrationForm, UserLoginForm, UserPasswordResetForm, UserPasswordChangeForm, UserSetPasswordForm, StudentForm
# Create your views here.

def index(request):
    # Page from the theme
    return render(request, 'pages/index.html')

def abouts_us(request):
    return render(request, 'pages/about.html')

def what_we_do(request):
    return render(request, 'pages/what_we_do.html')

def appattack(request):
    return render(request, 'pages/appattack/main.html')

def appattack_join(request):
    return render(request, 'pages/appattack/join.html')

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

def faq(request):
     # Page from the theme
    return render(request, 'pages/pt_gui/faq.html')

def ptgui_join_us(request):
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
    return render(request, 'pages/joinus.html', context)
    
def smishingdetection(request):
    return render(request, 'pages/smishing_detection/main.html')

def smishingdetection_join_us(request):
    return render(request, 'pages/smishing_detection/join_us.html')

# Upskill Pages
def upskill_repository(request):
    return render(request), 'pages/upskilling/repository.html'

def upskill_roadmap(request):
    return render(request), 'pages/upskilling/roadmap.html'

def upskill_progress(request):
    return render(request), 'pages/upskilling/progress.html'



# Authentication
class UserLoginView(LoginView):
    template_name = 'accounts/sign-in.html'
    form_class = UserLoginForm

def logout_view(request):
    logout(request)
    return redirect('/')

def register(request):
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

def resources_view(request):
    return render(request, 'pages/resources.html.')
    

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


def statistics_view(request):
    return render(request, 'charts/statistics.html')

def contact(request):
    if request.method=='POST':
        name=request.POST['name']
        email=request.POST['email']
        message=request.POST['message']
        contact=Contact.objects.create(name=name, email=email, message=message)
        messages.success(request,'The message has been received')
    return render(request,'pages/index.html')