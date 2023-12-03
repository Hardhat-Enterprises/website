from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('malware_viz', views.malwarehome, name='malware_viz_main'),
]


