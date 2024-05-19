from django.urls import path
from django.contrib import admin
from .views import Index, DetailArticleView, LikeArticle, UpskillingView, UpskillingSkillView

from . import views

urlpatterns = [
    path('', views.index, name='index'),

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

    path('smishing_detection/join_us', views.smishingdetection_join_us, name='smishingdetection_join_us'),

   path('upskill/repository', views.upskill_repository, name='pages/upskilling/repository.html'),
   path('upskill/roadmap', views.upskill_repository, name='pages/upskilling/roadmap.html'),
   path('upskill/progress', views.upskill_repository, name='pages/upskilling/progress.html'),
   path('dashboard/', views.dashboard, name='dashboard'),



    # path('contact-central/', views.Contact_central, name='contact-central'),
    
    
    # Search result page
    path('search_results/', views.search_results, name='pages/search-results'),
    path('website-form/', views.website_form, name='pages/website-form'),

    # Blog URLs
    path('blog/', Index.as_view(), name = 'blog'),
    path('<int:pk>/', DetailArticleView.as_view(), name='detail_article' ),
    path('<int:pk>/like', LikeArticle.as_view(), name='like_article'),
    
    # Email OTP
    
    path("verifyEmail/", views.VerifyOTP, name="verifyEmail"),
   


    #Statistics
    path('chart/filter-options', views.get_filter_options, name='chart-filter-options'),
    path('chart/project-priority/<str:priority>', views.get_priority_breakdown, name='chart-filter-options'),
    path('stats', views.statistics_view, name='project-stats'),
    path('ptgui_viz/join_us', views.ptgui_join_us, name='ptgui_join_us'),

]

