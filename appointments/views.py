from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import AppointmentForm
from .models import Appointment

def book_counselling(request):
    if request.method == "POST":
        form = AppointmentForm(request.POST)
        if form.is_valid():
            try:
                appt = form.save()
                messages.success(request, "Your appointment was created.")
                return redirect("career-counselling-confirm", appt_id=appt.id)
            except Exception as e:
                # UniqueConstraint (duplicate slot) or any DB error
                messages.error(request, "That slot is already booked. Please pick a different time.")
    else:
        form = AppointmentForm()
    return render(request, "appointments/booking_form.html", {"form": form})

def booking_confirm(request, appt_id):
    appt = get_object_or_404(Appointment, id=appt_id)
    return render(request, "appointments/confirm.html", {"appt": appt})
