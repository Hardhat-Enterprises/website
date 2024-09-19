from django.shortcuts import render, redirect, get_object_or_404
from .forms import SignUpForm, LoginForm
from django.contrib.auth import authenticate, login
from account.models import User
from django.http import JsonResponse
# Create your views here.


def index(request):
    return render(request, 'index.html')


def register(request):
    msg = None
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            msg = 'user created'
            return redirect('login_view')
        else:
            msg = 'form is not valid'
    else:
        form = SignUpForm()
    return render(request,'register.html', {'form': form, 'msg': msg})

def add(request):
    msg = None
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            msg = 'user created'
            return redirect('adminpage')
        else:
            msg = 'form is not valid'
    else:
        form = SignUpForm()
    return render(request,'add.html', {'form': form, 'msg': msg})


def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and user.is_platform_leader:
                login(request, user)
                return redirect('platform_leader_page')
            elif user is not None and user.is_platform_senior_developer:
                login(request, user)
                return redirect('psd')
            elif user is not None and user.is_platform_general_developer:
                login(request, user)
                return redirect('pgd')
            else:
                msg= 'No Permission'
        else:
            msg = 'error validating form'
    return render(request, 'login.html', {'form': form, 'msg': msg})


def delete_user(request, user_id):
    if request.method == 'POST':
        user = get_object_or_404(User, id=user_id)
        user.delete()
        return JsonResponse({"success": True})  # Return a success response for AJAX
    return JsonResponse({"success": False}, status=400)
# def admin(request):
#     return render(request,'admin.html')
def admin(request):
    users = User.objects.all()  # Fetch all users from the database
    return render(request, 'platform_leader.html', {'users': users})

def customer(request):
    users = User.objects.all()
    return render(request,'psd.html', {'users': users})


def employee(request):
    users = User.objects.all()
    return render(request,'pgd.html', {'users': users})