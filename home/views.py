# from django.shortcuts import render, get_object_or_404
 
# views.py
 
from django.shortcuts import render, redirect, get_object_or_404
 
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required

from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetView, PasswordResetConfirmView, PasswordResetDoneView, PasswordResetCompleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
from django.db.models import Count
from django.http import JsonResponse
from django.contrib import messages
from django.views import View
from django.views.generic import ListView, DetailView
from django.views.decorators.csrf import csrf_exempt
from .models import Article, Student, Project, Contact, Smishingdetection_join_us, Projects_join_us, Webpage 
 
from .models import Article, Student, Project, Contact, Smishingdetection_join_us, Webpage
from django.contrib.auth import get_user_model
from .models import User
from django.utils import timezone
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse_lazy
# from Website.settings import EMAIL_HOST_USER
import random

import os
import json
# from utils.charts import generate_color_palette
# from .models import Student, Project, Contact
from .forms import RegistrationForm, UserLoginForm, UserPasswordResetForm, UserPasswordChangeForm, UserSetPasswordForm, StudentForm, sd_JoinUsForm, projects_JoinUsForm, NewWebURL


 
 
# import os
 
from .models import Smishingdetection_join_us, DDT_contact
# import json
 
 
# from utils.charts import generate_color_palette
# from .models import Student, Project, Contact
# from .forms import RegistrationForm, UserLoginForm, UserPasswordResetForm, UserPasswordChangeForm, UserSetPasswordForm, StudentForm, sd_JoinUsForm, NewWebURL
 
 

from utils.charts import generate_color_palette, colorPrimary, colorSuccess, colorDanger
from utils.passwords import gen_password
from .models import Student, Project, Progress, Skill
 
#from .models import Student, Project, Progress
 
 
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
    return render(request, 'pages/joinus.html', context)
 
def smishing_detection(request):
    return render(request, 'pages/smishing_detection/main.html')
 
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
 
#Search-Results page
def search_results(request):
    if request.method == "POST":
        searched = request.POST['searched']
       
        webpages = Webpage.objects.filter(title__contains=searched)
        return render(request, 'pages/search-results.html',
            {'searched':searched,
            'webpages':webpages})
    else:
        return render(request, 'pages/search-results.html', {})
   
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

def Vr_main(request):
    return render(request, 'pages/Vr/main.html')

# Authentication



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
 
def logout_view(request):
    logout(request)
    return redirect('/')
 
def password_gen(request):
    return JsonResponse({'data': gen_password()}, status=200)
 
 
def register(request):
    form = RegistrationForm()
    if request.method == 'POST':
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        form = RegistrationForm(request.POST)
       
        if form.is_valid():
            form.save()
            otp = random.randint(100000, 999999)
            send_mail("User Data:", f"Hello from HardHat Enterprise! Verify Your Mail with the OTP: \n {otp}\n" f"If you didn't request an OTP or open an account with us, please contact us at your earliest convenience.\n\n"
                    "Regards, \nHardhat Enterprises", "deakinhardhatwebsite@gmail.com", [email], fail_silently=False)
            print("Account created successfully! An OTP was sent to your email. Check!")
            messages.success(request, "Account created successfully!")
            return render(request, 'accounts/verify_token.html', {'otp': otp, 'first_name': first_name, 'last_name': last_name, 'email': email, 'password1': password1, 'password2': password2})
            # return redirect("verify-email", username=request.POST['first_name'])
        else:
            print("Registration failed!")
    else:
        form = RegistrationForm()
 
    context = { 'form': form }
    return render(request, 'accounts/sign-up.html', context)
 
@csrf_exempt
def VerifyOTP(request):
    if request.method == "POST":
        userotp = request.POST.get('otp')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
       
        if password1 == password2:
            form = User(first_name=first_name, last_name=last_name, email=email, password=password1)
            form.save()
           
        print("OTP: ", userotp)
    return JsonResponse({'data': 'Hello'}, status=200)  
   
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
# def verify_email(request, first_name):
#     user = get_user_model().objects.get(username=first_name)
#     user_otp = OtpToken.objects.filter(user=user).last()
    
    
#     if request.method == 'POST':
#         # valid token
#         if user_otp.otp_code == request.POST['otp_code']:
            
#             # checking for expired token
#             if user_otp.otp_expires_at > timezone.now():
#                 user.is_active=True
#                 user.save()
#                 messages.success(request, "Account activated successfully!! You can Login.")
#                 return redirect("signin")
            
#             # expired token
#             else:
#                 messages.warning(request, "The OTP has expired, get a new OTP!")
#                 return redirect("verify-email", username=user.first_name)
        
        
#         # invalid otp code
#         else:
#             messages.warning(request, "Invalid OTP entered, enter a valid OTP!")
#             return redirect("verify-email", username=user.first_name)
        
#     context = {}
#     return render(request, "verify_token.html", context)


# def resend_otp(request):
#     if request.method == 'POST':
#         user_email = request.POST["otp_email"]
        
#         if get_user_model().objects.filter(email=user_email).exists():
#             user = get_user_model().objects.get(email=user_email)
#             otp = OtpToken.objects.create(user=user, otp_expires_at=timezone.now() + timezone.timedelta(minutes=5))
            
            
#             # email variables
#             subject="Email Verification"
#             message = f"""
#                                 Hi {user.username}, here is your OTP {otp.otp_code} 
#                                 it expires in 5 minute, use the url below to redirect back to the website
#                                 http://127.0.0.1:8000/verify-email/{user.username}
                                
#                                 """
#             sender = "kaviuln@gmail.com"
#             receiver = [user.email, ]
        
        
#             # send email
#             send_mail(
#                     subject,
#                     message,
#                     sender,
#                     receiver,
#                     fail_silently=False,
#                 )
            
#             messages.success(request, "A new OTP has been sent to your email-address")
#             return redirect("verify-email", username=user.first_name)

#         else:
#             messages.warning(request, "This email dosen't exist in the database")
#             return redirect("resend-otp")
        
           
#     context = {}
#     return render(request, "resend_otp.html", context)



 
 
 
 
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
    try:
        student = Student.objects.get(user=user)
    except Student.DoesNotExist:
        return redirect('/joinus')
    progress = Progress.objects.filter(student=student)
    context = {'user': user, 'student': student, 'progress': progress}
    return render(request, 'pages/dashboard.html', context)
 
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
 
 
 
 
class UpskillingView(LoginRequiredMixin, ListView):
    login_url = '/accounts/login/'
    model = Skill
    template_name = 'pages/upskilling.html'  
 
    def get_queryset(self):
        if self.request.user.is_authenticated:
            student = Student.objects.get(user=self.request.user)
            # Get the progress objects for the student
            progress = Progress.objects.filter(student=student)
            # Return the associated skills
            return [p.skill for p in progress]
        else:
            return self.model.objects.none()
 
class UpskillingSkillView(LoginRequiredMixin, DetailView):
    login_url = '/accounts/login/'  
    model = Skill
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
 
    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            student = Student.objects.get(user=self.request.user)
            # Check if the progress objects for the student exist
            if not Progress.objects.filter(student=student).exists():
                # If not, redirect to the home page
                return redirect('/')
            try:
                # Get the progress associated with the student and the current skill
                progress = Progress.objects.get(student=student, skill=self.get_object())
                # If progress does not exist, redirect to home page
            except Progress.DoesNotExist:
                return redirect('/')
        # Otherwise, proceed as usual
        return super().get(request, *args, **kwargs)
 
    def get_template_names(self):
        return [f'pages/upskilling/{self.kwargs["slug"]}_skill.html']
 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
 
        if self.request.user.is_authenticated:
            # Get the student
            student = Student.objects.get(user=self.request.user)
 
            # Get the progress associated with the student and the current skill
            progress = Progress.objects.get(student=student, skill=self.object)
            # Add the progress_id to the context
            context['progress_id'] = progress.id


        return context


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

 
       # return context

#Search suggestion ~ Raja Singh
def search_suggestions(request):
    if 'term' in request.GET:
        term = request.GET.get('term')
        # Filter the Webpage model by title containing the search term
        webpages = Webpage.objects.filter(title__icontains=term)[:5]
        suggestions = []
        for webpage in webpages:
            suggestions.append({
                'title': webpage.title,
                 'url': webpage.url or 'URL not available'
            })
        return JsonResponse(suggestions, safe=False)