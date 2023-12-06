from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def index(request):
    # Page from the theme
    return render(request, 'pages/index.html')


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


def http_503(request):
    return render(request, 'pages/503.html')
