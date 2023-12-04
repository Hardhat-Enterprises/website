from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def index(request):
<<<<<<< HEAD

    # Page from the theme
    return render(request, 'pages/index.html')


def malwarehome(request):

    # Page from the theme
    return render(request, 'pages/malware_visualization/main.html')


def malwareform(request):

    # Page from the theme
    return render(request, 'pages/malware_visualization/malware_viz_form.html')
=======
    # Page from the theme 
    return render(request, 'pages/index.html')

def products_services(request):
    # Page from the theme 
    return render(request, 'pages/malware_visualization/products_and_services.html')

def malwarehome(request):

    # Page from the theme 
    return render(request, 'pages/malware_visualization/main.html')
>>>>>>> 0ac3b8bf6d1604da69002b656140ccba1268e38f
