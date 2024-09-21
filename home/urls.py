from django.urls import path
from django.contrib import admin

from .views import Index, DetailArticleView, LikeArticle,  AddArticlecomment, CreateArticleView, UpdateArticleView, DeleteArticleView, UpskillingView, UpskillingSkillView, SearchResults, UpskillSuccessView, UpskillingJoinProjectView, join_project


from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('profile/', views.profile, name='profile'),
    path('malware_viz/joinus', views.malware_joinus, name='malware_viz_joinus'),
    path('appattack/', views.appattack, name='appattack'),
    path('appattack/join', views.appattack_join, name='appattack_join'),
    path('malware_viz/products_and_services',
         views.products_services, name='malware_products'),
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
    path('blog/', Index.as_view(), name = 'blog'),
    path('<int:pk>/', DetailArticleView.as_view(), name='detail_article' ),
    path('blog/edit/<int:pk>/', UpdateArticleView.as_view(), name='update_article' ),
    path('blog/<int:pk>/remove', DeleteArticleView.as_view(), name='delete_article' ),
    path('blog/add_blog/', CreateArticleView.as_view(), name='add_blog'),
    path('blog/<int:pk>/like', LikeArticle.as_view(), name='like_article'),
    path('blog/<int:article_id>/comment', AddArticlecomment, name='add_comment'),

    # Email OTP
    path("verifyEmail/", views.VerifyOTP, name="verifyEmail"),
 
    #Statistics
    path('chart/filter-options', views.get_filter_options, name='chart-filter-options'),
    path('chart/project-priority/<str:priority>', views.get_priority_breakdown, name='chart-filter-options'),
    path('stats', views.statistics_view, name='project-stats'),
    path('ptgui_viz/join_us', views.ptgui_join_us, name='ptgui_join_us'),

    path('feedback/', views.feedback, name='feedback'),

] 
    path('challenges/', views.challenge_list, name='challenge_list'),
    path('challenges/<str:category>/', views.category_challenges, name='category_challenges'),
    path('challenges/detail/<int:challenge_id>/', views.challenge_detail, name='challenge_detail'),
    path('challenges/<int:challenge_id>/submit/', views.submit_answer, name='submit_answer'),


    #Feedback
    path('feedback/', views.feedback_view, name='feedback'),
    path('submit-feedback/', views.submit_feedback, name='submit_feedback'),


]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

