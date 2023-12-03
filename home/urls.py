from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
<<<<<<< HEAD
    path('malware_viz/products_and_services', views.products_services, name='malware_products'),
=======
    path('malware_viz', views.malwarehome, name='malware_viz_main'),
>>>>>>> 658d4be760c453d49c906210e35d451585d9e777
]


