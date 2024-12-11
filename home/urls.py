from django.urls import include, path

from django.contrib import admin
from .views import Index, DetailArticleView, LikeArticle, UpskillingView, UpskillingSkillView, SearchResults, UpskillSuccessView, UpskillingJoinProjectView, join_project, list_careers,career_detail,career_application, feedback_view, delete_feedback
from django.conf import settings
from django.conf.urls.static import static
from django_ratelimit.decorators import ratelimit
from .views import UserLoginView, rate_limit_exceeded

#from home.views import register
from rest_framework.routers import DefaultRouter
from .views import APIModelListView
from .views import AnalyticsAPI
from .views import UserManagementAPI, EmailNotificationViewSet
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'email-notifications', EmailNotificationViewSet, basename='email-notifications')
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('client_sign-in/', views.client_sign_in, name='client_sign_in'),
    path('profile/', views.profile, name='profile'),
    path('malware_viz/joinus', views.malware_joinus, name='malware_viz_joinus'),
    path('appattack/', views.appattack, name='appattack'),
    path('appattack/join', views.appattack_join, name='appattack_join'),
    path('malware_viz/products_and_services', views.products_services, name='malware_products'),
    path('malware_viz/', views.malwarehome, name='malware_viz_main'),
    path('ptgui_viz/', views.ptguihome, name='ptgui_viz_main'),
    path('ptgui_viz/contact-us/', views.ptgui_contact_us, name='ptgui_contact-us'),
    path('maintenance', views.http_503, name='maintenance'),
    path('ptgui_viz/faq/', views.faq, name='faq'),
    path('smishing_detection', views.smishing_detection, name='smishing_detection_main'),
    #path('smishing_detection/join_us', views.smishing_detection_join_us, name='smishingdetection_join_us'),
    path('upskilling/', UpskillingView.as_view(), name='upskilling'),
    path('upskilling/<slug:slug>/', UpskillingSkillView.as_view(), name='upskilling_skill'),
    path('update-progress/<int:progress_id>/', views.update_progress, name='update_progress'),
    path('join-us/', join_project, name='join_us'),
    path('success/', UpskillSuccessView, name='success'),
    path('smishing_detection/join_us', views.smishingdetection_join_us, name='smishingdetection_join_us'),
    path('deakinThreatmirror/', views.Deakin_Threat_mirror_main, name='Deakin_Threat_mirror_main'),
    path('deakinThreatmirror/join_us', views.Deakin_Threat_mirror_joinus, name='threat_mirror_join_us'),
    path('vr/', views.Vr_main, name='Vr_main'),
    path('vr/join_us', views.vr_join_us, name='cybersafe_vr_join_us'),
    # path('contact-central/', views.Contact_central, name='contact-central'),
    path('accounts/password-reset/', views.UserPasswordResetView.as_view(), name='password_reset'),
    path('accounts/password-reset-confirm/<uidb64>/<token>/', views.UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),


     path('upskill/repository', views.upskill_repository, name='pages/upskilling/repository.html'),
     path('upskill/roadmap', views.upskill_repository, name='pages/upskilling/roadmap.html'),
     path('upskill/progress', views.upskill_repository, name='pages/upskilling/progress.html'),
     path('dashboard/', views.dashboard, name='dashboard'),



    # path('contact-central/', views.Contact_central, name='contact-central'),
    
    
    # Search result page
    path('SearchResults/', views.SearchResults, name='pages/search-results'),
    path('website_form/', views.website_form, name='pages/website-form'),
    
    # Search Suggestions
    path('search/suggestions/', views.SearchSuggestions, name='SearchSuggestions'),
    
    # Blog URLs
    path("careers/", list_careers , name="career-list"),
    path("careers/<int:id>/", career_detail , name="career-detail"),
    path("careers/<int:id>/apply", career_application , name="career-application"),
    
    path('blog/', Index.as_view(), name = 'blog'),
    path('<int:pk>/', DetailArticleView.as_view(), name='detail_article' ),
    path('<int:pk>/like', LikeArticle.as_view(), name='like_article'),
    

    # Login
    path('accounts/signup/', views.register, name='signup'),
    path('captcha/', include('captcha.urls')), 
    path('post-otp-captcha/', views.post_otp_login_captcha, name='post_otp_login_captcha'),


    # Email OTP
    
    
    # Email OTP
    path("verifyEmail/", views.VerifyOTP, name="verifyEmail"),
    path('accounts/login/', views.login_with_otp, name='login_with_otp'),
    path('accounts/verify-otp/', views.verify_otp, name='verify_otp'),
    # Statistics
    path('chart/filter-options', views.get_filter_options, name='chart-filter-options'),
    path('chart/project-priority/<str:priority>', views.get_priority_breakdown, name='chart-filter-options'),
    path('stats', views.statistics_view, name='project-stats'),
    path('ptgui_viz/join_us', views.ptgui_join_us, name='ptgui_join_us'),
    
    path('feedback/', views.feedback, name='feedback'),



    path('challenges/', views.challenge_list, name='challenge_list'),
    path('challenges/<str:category>/', views.category_challenges, name='category_challenges'),
    path('challenges/detail/<int:challenge_id>/', views.challenge_detail, name='challenge_detail'),
    path('challenges/<int:challenge_id>/submit/', views.submit_answer, name='submit_answer'),
    
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    
    # Feedback (duplicate removed)

    # path('submit-feedback/', views.submit_feedback, name='submit_feedback'),


    path('accounts/login/', UserLoginView.as_view(), name='login'),
    path('rate_limit_exceeded/', rate_limit_exceeded, name='rate_limit_exceeded'),
 


    #swagger-new-implementation
    path('api-models/', APIModelListView.as_view(), name='api-models'),
    path('api-analytics/', AnalyticsAPI.as_view(), name='api-analytics'),
    path('user-management/', UserManagementAPI.as_view(), name='user-management'),
    path('', include(router.urls)), 
    path('feedback/', views.feedback_view, name='feedback'),
    path('feedback/delete/<int:id>', delete_feedback, name='delete_feedback')

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


