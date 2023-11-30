from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):

    # Page from the theme 
    return render(request, 'pages/index.html')

def register_view(request):
    return render(request, 'pages/register.html')

def login_view(request):
    return render(request, 'pages/login.html')