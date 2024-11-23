"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views
from home import views

from .admin import admin_statistics_view

handler404 = 'home.views.error_404_view'

urlpatterns = [
    path("admin/statistics/", admin.site.admin_view(admin_statistics_view), name="admin-statistics"),
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    # path('', include('theme_pixel.urls')),
    path('about-us/', views.about_us, name='about_us'),
    path('contact', views.contact, name='contact'),
    path('contact-central', views.Contact_central, name='contact-central'),
    path('joinus/', views.join_project, name='join-project'),
    path('what-we-do/', views.what_we_do, name='what_we_do'),
    
    # blog
    #path('admin/', admin.site.urls),
    # path('blog/', include('blogs.urls')),
    #path('', include('blogs.urls')),
    #path('accounts/', include('users.urls')),
    path('blog/', views.blog, name='blog'),
    path('tinymce/', include('tinymce.urls')),
    
    path("verifyEmail/", views.VerifyOTP, name="verifyEmail"),

    # Authentication
    path('accounts/login/', views.UserLoginView.as_view(), name='login'),
    path('accounts/logout/', views.logout_view, name='logout'),
    path('accounts/register/', views.register, name='register'),
    path('accounts/password-gen/', views.password_gen, name='password_gen'),
    path('accounts/password-change/', views.UserPasswordChangeView.as_view(), name='password_change'),
    path('accounts/password-change-done/', auth_views.PasswordChangeDoneView.as_view(
        template_name = 'accounts/password_change_done.html'
    ), name='password_change_done'),
    path('accounts/password-reset/', views.UserPasswordResetView.as_view(), name='password_reset'),
    path('accounts/password-reset-done/', auth_views.PasswordResetDoneView.as_view(
        template_name='accounts/password_reset_done.html'
    ), name='password_reset_done'),
    path('accounts/password-reset-confirm/<uidb64>/<token>/', 
       views.UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('accounts/password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='accounts/password_reset_complete.html'
    ), name='password_reset_complete'),
    path('comphrensive-report', views.comphrehensive_reports, name='comphrehensive_report'),
    path('pen-testing', views.pen_testing, name='pen-testing'),
    path('secure-code-review', views.secure_code_review, name='secure-code-review'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('update_progress/<int:progress_id>/', views.update_progress, name='update_progress'),

]


