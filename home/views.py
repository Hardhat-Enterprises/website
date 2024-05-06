# from django.shortcuts import render, get_object_or_404

# views.py

from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetView, PasswordResetConfirmView
from django.contrib.auth import logout
from django.db.models import Count
from django.http import JsonResponse
from django.contrib import messages
from django.views import View
from django.views.generic import ListView, DetailView

from .models import Article, Student, Project, Contact, Smishingdetection_join_us
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.mail import send_mail


import os



# from utils.charts import generate_color_palette
# from .models import Student, Project, Contact
from .forms import RegistrationForm, UserLoginForm, UserPasswordResetForm, UserPasswordChangeForm, UserSetPasswordForm, StudentForm


from utils.charts import generate_color_palette, colorPrimary, colorSuccess, colorDanger
from .models import Student, Project, Progress, OtpToken

# from .forms import RegistrationForm, UserLoginForm, UserPasswordResetForm, UserPasswordChangeForm, UserSetPasswordForm, StudentForm
# Create your views here.

# Regular Views


def index(request):
    return render(request, 'pages/index.html')

def about_us(request):
    return render(request, 'pages/about.html')

def what_we_do(request):
    return render(request, 'pages/what_we_do.html')

def blog(request):
    return render(request, 'blog/index.html')

def appattack(request):
    return render(request, 'pages/appattack/main.html')

def appattack_join(request):
    return render(request, 'pages/appattack/join.html')

def products_services(request):
    return render(request, 'pages/malware_visualization/products_and_services.html')

def malwarehome(request):
    return render(request, 'pages/malware_visualization/main.html')

def malware_joinus(request):
    return render(request, 'pages/malware_visualization/malware_viz_joinus.html')

def ptguihome(request):
    return render(request, 'pages/pt_gui/main.html')

def ptgui_contact_us(request):
    return render(request, 'pages/pt_gui/contact-us.html')

def faq(request):
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

def smishing_detection(request):
    return render(request, 'pages/smishing_detection/main.html')

def smishing_detection_join_us(request):

    
     if request.method=='POST':
        name=request.POST['name']
        email=request.POST['email']
        message=request.POST['message']

        if len(name)<2 or len(email)<3 or len(message)<4:
            messages.error(request, "Please fill the form correctly")
        else:
            contact= Smishingdetection_join_us(name=name, email=email, message=message)
            contact.save()
            messages.success(request, "Your message has been successfully sent") 
     return render(request, 'pages/smishing_detection/join_us.html')

# Upskill Pages
def upskill_repository(request):
    return render(request), 'pages/upskilling/repository.html'

def upskill_roadmap(request):
    return render(request), 'pages/upskilling/roadmap.html'

def upskill_progress(request):
    return render(request), 'pages/upskilling/progress.html'

#Search-Results page

def search_results(request):
    if request.method == 'POST':
        searched = request.POST['q']
        return render(request, 'pages/search-results.html', {"searched" :searched})
    else:
        return render(request, 'pages/search-results.html', {})
    


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
            print("Account created successfully! An OTP was sent to your email. Check!")
            # messages.success(request, "Account created successfully! An OTP was sent to your email! check message")
            return redirect('/accounts/login')
           # return redirect('/accounts/verify_token')
        else:
            print("Registration failed!")
    else:
        form = RegistrationForm()

    context = { 'form': form }
    return render(request, 'accounts/sign-up.html', context)

# def signup(request):
#     form = RegisterForm()
#     if request.method == 'POST':
#         form = RegisterForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Account created successfully! An OTP was sent to your Email")
#             return redirect("verify-email", username=request.POST['username'])
#     context = {"form": form}
#     return render(request, "signup.html", context)


# Email Verification 
def verify_email(request, username):
    user = get_user_model().objects.get(username=username)
    user_otp = OtpToken.objects.filter(user=user).last()
    
    
    if request.method == 'POST':
        # valid token
        if user_otp.otp_code == request.POST['otp_code']:
            
            # checking for expired token
            if user_otp.otp_expires_at > timezone.now():
                user.is_active=True
                user.save()
                messages.success(request, "Account activated successfully!! You can Login.")
                return redirect("signin")
            
            # expired token
            else:
                messages.warning(request, "The OTP has expired, get a new OTP!")
                return redirect("verify-email", username=user.username)
        
        
        # invalid otp code
        else:
            messages.warning(request, "Invalid OTP entered, enter a valid OTP!")
            return redirect("verify-email", username=user.username)
        
    context = {}
    return render(request, "verify_token.html", context)


def resend_otp(request):
    if request.method == 'POST':
        user_email = request.POST["otp_email"]
        
        if get_user_model().objects.filter(email=user_email).exists():
            user = get_user_model().objects.get(email=user_email)
            otp = OtpToken.objects.create(user=user, otp_expires_at=timezone.now() + timezone.timedelta(minutes=5))
            
            
            # email variables
            subject="Email Verification"
            message = f"""
                                Hi {user.username}, here is your OTP {otp.otp_code} 
                                it expires in 5 minute, use the url below to redirect back to the website
                                http://127.0.0.1:8000/verify-email/{user.username}
                                
                                """
            sender = "kaviuln@gmail.com"
            receiver = [user.email, ]
        
        
            # send email
            send_mail(
                    subject,
                    message,
                    sender,
                    receiver,
                    fail_silently=False,
                )
            
            messages.success(request, "A new OTP has been sent to your email-address")
            return redirect("verify-email", username=user.username)

        else:
            messages.warning(request, "This email dosen't exist in the database")
            return redirect("resend-otp")
        
           
    context = {}
    return render(request, "resend_otp.html", context)


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

def comphrehensive_reports(request):
    # Page from the theme
    return render(request, 'pages/appattack/comprehensive_reports.html')

def pen_testing(request):
    # Page from the theme
    return render(request, 'pages/appattack/pen_testing.html')

def secure_code_review(request):
    # Page from the theme
    return render(request, 'pages/appattack/secure_code_review.html')

@login_required
def dashboard(request):
    user = request.user
    student = Student.objects.get(user=user)
    progress = Progress.objects.filter(student=student)
    context = {'user': user, 'student': student, 'progress': progress}
    return render(request, 'pages/dashboard.html', context)

def update_progress(request, progress_id):
    progress = get_object_or_404(Progress, id=progress_id)
    if request.method == 'POST':
        new_progress = request.POST.get('progress')
        progress.progress = new_progress
        progress.save()
    return redirect('dashboard')

def contact(request):
    if request.method=='POST':
        name=request.POST['name']
        email=request.POST['email']
        message=request.POST['message']
        contact=Contact.objects.create(name=name, email=email, message=message)
        messages.success(request,'The message has been received')
    return render(request,'pages/index.html')

def Contact_central(request):
    if request.method=='POST':
        name=request.POST['name']
        email=request.POST['email']
        message=request.POST['message']
        contact=Contact.objects.create(name=name, email=email, message=message)
        messages.success(request,'The message has been received')
    return render(request,'pages/Contactus.html')


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

