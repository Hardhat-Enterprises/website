from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name= 'index'),
    path('login/', views.login_view, name='login_view'),
    path('register/', views.register, name='register'),
    path('add/', views.add, name='add'),
    path('platform_leader_page/', views.admin, name='platform_leader_page'),
    path('psd/', views.customer, name='psd'),
    path('pgd/', views.employee, name='pgd'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
]