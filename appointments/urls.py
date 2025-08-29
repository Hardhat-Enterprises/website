from django.urls import path
from . import views

urlpatterns = [
    path("careers/counselling/", views.book_counselling, name="career-counselling"),
    path("careers/counselling/confirm/<int:appt_id>/", views.booking_confirm, name="career-counselling-confirm"),
]
