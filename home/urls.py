from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('malware_viz/products_and_services', views.products_services, name='malware_products'),
]
