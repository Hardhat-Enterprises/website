from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),

    path('malware_viz/joinus', views.malware_joinus, name='malware_viz_joinus'),
    path('appattack/', views.appattack, name='appattack'),
    path('appattack/join', views.appattack_join, name='appattack_join'),
    path('malware_viz/products_and_services',
         views.products_services, name='malware_products'),
    path('malware_viz', views.malwarehome, name='malware_viz_main'),
    path('ptgui_viz', views.ptguihome, name='ptgui_viz_main'),
    path('ptgui_viz/contact-us/', views.ptgui_contact_us, name='ptgui_contact-us'),
    path('maintenance', views.http_503, name='maintenance'),
    path('ptgui_viz/faq/', views.faq, name='faq'),
    path('smishing_detection', views.smishingdetection, name='smishing_detection_main'),
    path('smishing_detection/join_us', views.smishingdetection_join_us, name='smishingdetection_join_us'),
    path('upskill/repository', views.upskill_repository, name='pages/upskilling/repository.html'),
    path('upskill/roadmap', views.upskill_repository, name='pages/upskilling/roadmap.html'),
    path('upskill/progress', views.upskill_repository, name='pages/upskilling/progress.html'),

    #Statistics
    path('chart/filter-options', views.get_filter_options, name='chart-filter-options'),
    path('chart/project-priority/<str:priority>', views.get_priority_breakdown, name='chart-filter-options'),
    path('stats', views.statistics_view, name='project-stats'),
    path('ptgui_viz/join_us', views.ptgui_join_us, name='ptgui_join_us'),

]

