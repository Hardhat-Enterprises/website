from django.urls import path
from . import views

urlpatterns = [
    path('chat/', views.chat_view, name='chat_view'),
    path('api/session/create/', views.session_create_api, name='session_create_api'),
    path('api/session/<str:session_id>/', views.session_detail_api, name='session_detail_api'),
    path('api/session/<str:session_id>/message/', views.message_api, name='message_api'),
    path('analyze-fuzzy/', views.analyze_fuzzy_search, name='analyze_fuzzy_search'),
    path('api/analyze-text/', views.analyze_text_api, name='analyze_text_api'),
    path('api/verify/', views.verify_connection_api, name='verify_connection_api'),
    path('api/config/', views.chatbot_config_api, name='chatbot_config_api'),
]
