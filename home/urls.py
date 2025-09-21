from django.urls import include, path
from django.conf.urls.i18n import set_language

from django.contrib import admin

from .views import Index, DetailArticleView, LikeArticle, UpskillingView, UpskillingSkillView, SearchResults, UpskillSuccessView, UpskillingJoinProjectView, join_project, list_careers, internships, job_alerts, career_detail, career_application, feedback_view, delete_feedback, career_discover, policy_deployment
from .views import resources_view  
from django.conf import settings
from django.conf.urls.static import static
from django_ratelimit.decorators import ratelimit
from .views import UserLoginView, AdminLoginView, rate_limit_exceeded, admin_dashboard, ChallengeManagementView
from .views import delete_account

from django.conf.urls.static import static

# Health Endpoint Work
from .views import health_check
from django.views.i18n import set_language

from .views import ResourceListView




#from home.views import register
from rest_framework.routers import DefaultRouter
from .views import APIModelListView
from .views import AnalyticsAPI
from .views import UserManagementAPI, EmailNotificationViewSet
from .views import MarkSkillCompletedView
from .views import ChallengeListAPI, SkillListAPI, LeaderboardAPI, HealthCheckAPI

from rest_framework.routers import DefaultRouter
from .views import ResourceDetailView
router = DefaultRouter()
router.register(r'email-notifications', EmailNotificationViewSet, basename='email-notifications')
from . import views



urlpatterns = [
    path('', views.index, name='index'),
    path('client_sign-in/', views.client_sign_in, name='client_sign_in'),
    path('profile/', views.profile, name='profile'),
    path('profile/details/', views.profile_details, name='profile_details'),
    path('malware_viz/joinus', views.malware_joinus, name='malware_viz_joinus'),
    path('appattack/', views.appattack, name='appattack'),
    path('skills/', views.skills_view, name='Appattack_Skills'),
    path('appattack/join', views.appattack_join, name='appattack_join'),
    path('malware_viz/products_and_services', views.products_services, name='malware_products'),
    path('malware_viz/', views.malwarehome, name='malware_viz_main'),
    path('malware_viz/skills/', views.malware_skills, name='malware_skills'),
    path('ptgui_viz/', views.ptguihome, name='ptgui_viz_main'),
    path('ptgui_viz/skills/', views.ptgui_skills, name='ptgui_skills'),
    path('ptgui_viz/contact-us/', views.ptgui_contact_us, name='ptgui_contact-us'),
    path('maintenance', views.http_503, name='maintenance'),
    path('ptgui_viz/faq/', views.faq, name='faq'),
    path('ptgui_viz/tools/', views.tools_home, name='ptgui_tools_home'),
    path('ptgui_viz/tools/aircrack/', views.aircrack_view, name='tool_aircrack'),
    path('ptgui_viz/tools/arjun/', views.arjun_view, name='tool_arjun'),
    path('ptgui_viz/tools/rainbowcrack/', views.rainbow_view, name='tool_rainbowcrack'),
    path('ptgui_viz/tools/airbase/', views.airbase_view, name='tool_airbase'),
    path('ptgui_viz/tools/amap/', views.amap_view, name='tool_amap'),
    path('ptgui_viz/tools/amass/', views.amass_view, name='tool_amass'),
    path('ptgui_viz/tools/arpaname/', views.arpaname_view, name='tool_arpaname'),
    path('smishing_detection', views.smishing_detection, name='smishing_detection_main'),
    path('smishing_detection/skills/', views.smishing_skills, name='smishing_skills'),


     #path('smishing_detection/join_us', views.smishing_detection_join_us, name='smishingdetection_join_us'),
    path('upskilling/', UpskillingView.as_view(), name='upskilling'),
    path('upskilling/<slug:slug>/', UpskillingSkillView.as_view(), name='upskilling_skill'),
    path('update-progress/<int:progress_id>/', views.update_progress, name='update_progress'),
    path('join-us/', join_project, name='join_us'),
    path('success/', UpskillSuccessView, name='success'),
    path('smishing_detection/join_us', views.smishingdetection_join_us, name='smishingdetection_join_us'),
    path('deakinThreatmirror/', views.Deakin_Threat_mirror_main, name='Deakin_Threat_mirror_main'),
    path('deakinThreatmirror/skills/', views.deakinthreatmirror_skills, name='deakinthreatmirror_skills'),
    path('deakinThreatmirror/join_us', views.Deakin_Threat_mirror_joinus, name='threat_mirror_join_us'),
    path('vr/', views.Vr_main, name='Vr_main'),
    path('vr/skills/', views.cybersafe_vr_skills, name='cybersafe_vr_skills'),
    path('vr/join_us', views.vr_join_us, name='cybersafe_vr_join_us'),
    path('upskilling/complete/<slug:slug>/', MarkSkillCompletedView.as_view(), name='complete_skill'),
    # path('contact-central/', views.Contact_central, name='contact-central'),
    path('accounts/password-reset/', views.UserPasswordResetView.as_view(), name='password_reset'),
    path('accounts/password-reset-confirm/<uidb64>/<token>/', views.UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),


     path('upskill/repository', views.upskill_repository, name='pages/upskilling/repository.html'),
     path('upskill/roadmap', views.upskill_repository, name='pages/upskilling/roadmap.html'),
     path('upskill/progress', views.upskill_repository, name='pages/upskilling/progress.html'),
     path('dashboard/', views.dashboard, name='dashboard'),



    # path('contact-central/', views.Contact_central, name='contact-central'),
     path('appattack/join/', views.appattack_join, name='appattack_join'),
      path('form_success/', views.form_success, name='form_success'),
      path('policy-deployment/', views.policy_deployment, name='policy_deployment'),
    
    
    
    # Search result page
    path('SearchResults/', views.SearchResults, name='pages/search-results'),
    path('website_form/', views.website_form, name='pages/website-form'),
    
    # Search Suggestions
    path('search/suggestions/', views.SearchSuggestions, name='SearchSuggestions'),
    
    # Blog URLs
    path("careers/", list_careers , name="career-list"),
    path("careers/<int:id>/", career_detail , name="career-detail"),
    path("careers/<int:id>/apply", career_application , name="career-application"),
    path("careers/internships/", internships, name="internships"),
    path("careers/job-alerts/", job_alerts, name="job-alerts"),
    path("careers/discover/", career_discover, name="career-discover"),
    path("careers/path-finder/", views.career_path_finder, name="career_path_finder"),
    path("careers/graduate-program/", views.graduate_program, name="graduate-program"),
    path("careers/faqs/", views.careers_faqs, name="careers-faqs"),

    path('blog/', Index.as_view(), name = 'blog'),
    # path('blog/<int:pk>/', DetaswilArticleView.as_view(), name='blog_post'),
    path('<int:pk>/', DetailArticleView.as_view(), name='detail_article' ),
    path('<int:pk>/like', LikeArticle.as_view(), name='like_article'),
    

    # Login
    path('accounts/signup/', views.register, name='signup'),
    path('captcha/', include('captcha.urls')), 
    path('post-otp-captcha/', views.post_otp_login_captcha, name='post_otp_login_captcha'),
    path('accounts/passkey-login/', views.login_with_passkey, name='passkey_login'),
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
    path("passkeys/reset/", views.reset_passkeys_request, name="reset_passkeys_request"),
    path("passkeys/reset/verify/", views.reset_passkeys_verify, name="reset_passkeys_verify"),

    # Email OTP
    
    
    # Email OTP
    path("verifyEmail/", views.VerifyOTP, name="verifyEmail"),
    path('accounts/login/', views.login_with_otp, name='login_with_otp'),
    path('accounts/verify-otp/', views.verify_otp, name='verify_otp'),
    path('accounts/microsoft-login/', views.microsoft_login, name='microsoft_login'),
    # Statistics
    path('chart/filter-options', views.get_filter_options, name='chart-filter-options'),
    path('chart/project-priority/<str:priority>', views.get_priority_breakdown, name='chart-filter-options'),
    path('stats', views.statistics_view, name='project-stats'),
    path('ptgui_viz/join_us', views.ptgui_join_us, name='ptgui_join_us'),
    
 
    path('blogpage/', views.blogpage, name='blogpage'),
    path('blogpage/delete/<int:id>', views.delete_blogpage, name='delete_blogpage'),
    path('edit_blogpage/<int:id>/', views.edit_blogpage, name='edit_blogpage'),
    path('adminblogpage/', views.adminblogpage, name='adminblogpage'),
    path('adminblogpage/approve/<int:id>/', views.approve_blogpage, name='approve_blogpage'),
    path('adminblogpage/reject/<int:id>/', views.reject_blogpage, name='reject_blogpage'),
    path('publishedblog/', views.publishedblog, name='publishedblog'),
    path('report-blog/', views.report_blog, name='report_blog'),
    path('reports/', views.adminblogreports, name='reports'),
    path('reported/download/', views.download_reported_blogs, name='download_reported_blogs'),

    path('challenges/', views.challenge_list, name='challenge_list'),
    path('challenges/cyber-challenge/', views.cyber_challenge, name='cyber_challenge'),
    path('challenges/quiz/', views.cyber_quiz, name='cyber_quiz'),
    path('challenges/match/', views.cyber_match, name='cyber_match'),

    path('challenges/manage/', ChallengeManagementView.as_view(), name='challenge_management'),
    path('challenges/add/', views.ChallengeCreateView.as_view(), name='add_challenge'),

    path('challenges/<str:category>/', views.category_challenges, name='category_challenges'),
    path('challenges/detail/<int:challenge_id>/', views.challenge_detail, name='challenge_detail'),
    path('challenges/<int:challenge_id>/submit/', views.submit_answer, name='submit_answer'),
    path('challenges/manage/', views.ChallengeManagementView.as_view(), name='challenge_management'),
    path('challenges/add/', views.ChallengeCreateView.as_view(), name='challenge_create'),
    path('challenges/<int:pk>/edit/', views.ChallengeUpdateView.as_view(), name='challenge_edit'),
    path('challenges/<int:pk>/delete/', views.ChallengeDeleteView.as_view(), name='challenge_delete'),
    path('challenges/<int:pk>/archive/', views.ChallengeArchiveView.as_view(), name='challenge_archive'),
    path('challenges/<int:pk>/preview/', views.ChallengePreviewView.as_view(), name='challenge_preview'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    
    # Feedback (duplicate removed)

    # path('submit-feedback/', views.submit_feedback, name='submit_feedback'),


    path('accounts/login/', UserLoginView.as_view(), name='login'),
    path('rate_limit_exceeded/', rate_limit_exceeded, name='rate_limit_exceeded'),
  path('accounts/admin/', AdminLoginView.as_view(), name='admin_login'),
    path('admin/dashboard/', admin_dashboard, name='admin_dashboard'),
    

    #swagger-new-implementation
    path('api-models/', APIModelListView.as_view(), name='api-models'),
    path('api-analytics/', AnalyticsAPI.as_view(), name='api-analytics'),
    path('user-management/', UserManagementAPI.as_view(), name='user-management'),
    path('api-challenges/', ChallengeListAPI.as_view(), name='api-challenges'),
    path('api-skills/', SkillListAPI.as_view(), name='api-skills'),
    path('api-leaderboard/', LeaderboardAPI.as_view(), name='api-leaderboard'),
    path('api-health/', HealthCheckAPI.as_view(), name='api-health'),
    path('', include(router.urls)), 
    path('feedback/', views.feedback_view, name='feedback'),
    path('feedback/delete/<int:id>', delete_feedback, name='delete_feedback'),


    path("appattack/reports/", views.comphrehensive_reports, name="comphrehensive_reports"),
    path("appattack/pen-testing/", views.pen_testing, name="pen-testing"),
    path("appattack/secure-code-review/", views.secure_code_review, name="secure-code-review"),
    path('appattack/pen-testing-form/', views.pen_testing_form_view, name='pen_testing_form'),
    path('appattack/secure-code-review-form/', views.secure_code_review_form_view, name='secure_code_review_form'),

    path('account/delete/', delete_account, name='delete-account'),
    path('vault/', views.vault_view, name='vault'),
    path('vault/delete/<int:doc_id>/', views.delete_document, name='delete_document'),


    path("health", health_check, name="health-check"),
    path("debug-auth/", views.debug_auth_status, name="debug_auth_status"),
    
    # internationalization
    path('i18n/setlang/', set_language, name='set_language'),
    path("resources/", ResourceListView.as_view(), name="resources"),
    path("resources/<slug:slug>/", ResourceDetailView.as_view(), name="resource_detail"),
      path("resources/<int:pk>/download/", views.resource_download, name="resource_download"),
    path("resources/<slug:slug>/", views.ResourceDetailView.as_view(), name="resource_detail"),
    path("resources/", views.ResourceListView.as_view(), name="resources"),
  

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
