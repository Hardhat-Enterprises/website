from django.urls import path

from . import views


app_name = "event"


urlpatterns = [
    path("event/", views.user_click_event, name="evnet")
]
