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
from django.conf.urls.i18n import i18n_patterns
from django.urls import include, path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from home import views
from rest_framework import permissions
from home.views_securitytxt import security_txt
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.urls import path, re_path
from .admin import admin_statistics_view
from home.views_securitytxt import security_txt
from home.views_robotstxt import robots_txt

from .admin import admin_dashboard

handler404 = 'home.views.error_404_view'
schema_view = get_schema_view(
    openapi.Info(
        title="Hardhat Website API",
        default_version="v1",
        description="API documentation for the Hardhat Website",
        terms_of_service="https://www.hardhatenterprises.com/terms/",
        contact=openapi.Contact(email="support@hardhatenterprises.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/statistics/", admin.site.admin_view(admin_statistics_view), name="admin-statistics"),
    path("admin/dashboard/", admin.site.admin_view(admin_dashboard), name="admin-dashboard"),
    path('admin/', admin.site.urls),
    path('accounts/', include('home.urls')), 
    path('', include('home.urls')),
    path('about-us/', views.about_us, name='about_us'),
    path('our-tools/', views.security_tools, name='our_tools'),
    path('contact', views.contact, name='contact'),
    path('contact-central', views.Contact_central, name='contact-central'),
    path('joinus/', views.join_project, name='join-project'),
    path('what-we-do/', views.what_we_do, name='what_we_do'),
    path('plan/', views.package_plan, name='package_plan'),
    path('cyber_threat_simulation/', views.cyber_threat_simulation, name='cyber_threat_simulation'),
    path('secure_digital_practices/', views.secure_digital_practices, name='secure_digital_practices'),
    path('cybersecurity_awareness_reports/', views.cybersecurity_awareness_reports, name='cybersecurity_awareness_reports'),
    path('.well-known/security.txt', security_txt, name='security-txt'),
    path("robots.txt", robots_txt, name="robots-txt"),

    # blog
    path('blog/', views.blog, name='blog'),
    path('tinymce/', include('tinymce.urls')),
# Custom Microsoft OAuth login and callback
path('oauth/login/', views.microsoft_oauth_login, name='microsoft_oauth_login'),
path('oauth/callback/', views.microsoft_oauth_callback, name='microsoft_oauth_callback'),
# Override the social_django complete URL to use our custom handler (MUST be before social_django URLs)
path('complete/azuread-tenant-oauth2/', views.microsoft_oauth_callback, name='microsoft_oauth_callback_override'),
# Custom OAuth completion view for other backends
path('complete/<str:backend>/', views.oauth_complete_redirect, name='oauth_complete_redirect'),
# Python Social Auth URLs (Microsoft OAuth implementation)
path('', include(('social_django.urls', 'social_django'), namespace='social')),
    
    path("verifyEmail/", views.VerifyOTP, name="verifyEmail"),
    path("test-login/", views.test_login, name="test_login"),

    # Authentication
    path('accounts/login/', views.UserLoginView.as_view(), name='login'),
    path('accounts/clientlogin/', views.client_login, name='client_login'),
    path('accounts/logout/', views.logout_view, name='logout'),
    path('accounts/register/', views.register, name='register'),
    path('accounts/registerclient/', views.register_client, name='register_client'),
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
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('i18n/', include('django.conf.urls.i18n')),
    path('', include('home.urls')),
    path("api/tip/today/", views.tip_today, name="tip_today"),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static('/static/assets/', document_root=settings.BASE_DIR / 'custom_static/assets')


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)