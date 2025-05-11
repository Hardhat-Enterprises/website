from django.urls import path
from .views import log_event, analytics_dashboard

urlpatterns = [
    path("log/", log_event, name="log_event"),
    path("analytics/", analytics_dashboard, name="analytics_dashboard"),
]