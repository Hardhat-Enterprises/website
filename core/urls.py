from django.contrib import admin
from django.urls import include, path, re_path
from django.contrib.auth import views as auth_views

from home import views as home_views
from core.views import blacklisted_ips_view
from .admin import admin_statistics_view, admin_dashboard

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

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
    # Admin and dashboards
    path('admin/', admin.site.urls),
    path("admin/statistics/", admin.site.admin_view(admin_statistics_view), name="admin-statistics"),
    path("admin/dashboard/", admin.site.admin_view(admin_dashboard), name="admin-dashboard"),
    path('admin/statistics/', admin.site.admin_view(blacklisted_ips_view), name="blacklisted-ips"),

    # API docs
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # Static pages
    path('about-us/', home_views.about_us, name='about_us'),
    path('contact/', home_views.contact, name='contact'),
    path('contact-central/', home_views.Contact_central, name='contact-central'),
    path('joinus/', home_views.join_project, name='join-project'),
    path('what-we-do/', home_views.what_we_do, name='what_we_do'),
    path('plan/', home_views.package_plan, name='package_plan'),
    path('blog/', home_views.blog, name='blog'),

    # Threat dashboard & internal tools
    path('dashboard/', home_views.dashboard, name='dashboard'),
    path('update_progress/<int:progress_id>/', home_views.update_progress, name='update_progress'),

    # Auth
    path('accounts/login/', home_views.UserLoginView.as_view(), name='login'),
    path('accounts/clientlogin/', home_views.client_login, name='client_login'),
    path('accounts/logout/', home_views.logout_view, name='logout'),
    path('accounts/register/', home_views.register, name='register'),
    path('accounts/registerclient/', home_views.register_client, name='register_client'),
    path('accounts/password-gen/', home_views.password_gen, name='password_gen'),
    path('accounts/password-change/', home_views.UserPasswordChangeView.as_view(), name='password_change'),
    path('accounts/password-change-done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='accounts/password_change_done.html'
    ), name='password_change_done'),
    path('accounts/password-reset/', home_views.UserPasswordResetView.as_view(), name='password_reset'),
    path('accounts/password-reset-done/', auth_views.PasswordResetDoneView.as_view(
        template_name='accounts/password_reset_done.html'
    ), name='password_reset_done'),
    path('accounts/password-reset-confirm/<uidb64>/<token>/', 
         home_views.UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('accounts/password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='accounts/password_reset_complete.html'
    ), name='password_reset_complete'),

    # Security services
    path('comprehensive-report/', home_views.comphrehensive_reports, name='comphrehensive_report'),
    path('pen-testing/', home_views.pen_testing, name='pen-testing'),
    path('secure-code-review/', home_views.secure_code_review, name='secure-code-review'),

    # TinyMCE
    path('tinymce/', include('tinymce.urls')),

    # Verification
    path("verifyEmail/", home_views.VerifyOTP, name="verifyEmail"),

    # Include all other home URLs
    path('', include('home.urls')),
]
