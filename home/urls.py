from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),

    path('malware_viz/joinus', views.malware_joinus, name='malware_viz_joinus'),
    path('appattack/', views.appattack, name='appattack'),
    path('malware_viz/products_and_services',
         views.products_services, name='malware_products'),
    path('malware_viz', views.malwarehome, name='malware_viz_main'),
    path('ptgui_viz', views.ptguihome, name='ptgui_viz_main'),
    path('ptgui_viz/contact-us/', views.ptgui_contact_us, name='ptgui_contact-us'),
    path('maintenance', views.http_503, name='maintenance'),
]
