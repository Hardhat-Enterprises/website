from django.db import models

# Create your models here.
from django.db import models

class Counsellor(models.Model):
    name = models.CharField(max_length=80)
    title = models.CharField(max_length=120, blank=True)
    email = models.EmailField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

STATUS_CHOICES = [
    ("PENDING", "Pending"),
    ("CONFIRMED", "Confirmed"),
    ("CANCELLED", "Cancelled"),
]

class Appointment(models.Model):
    counsellor = models.ForeignKey(Counsellor, on_delete=models.PROTECT, related_name="appointments")
    date = models.DateField()
    time = models.TimeField()
    full_name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default="PENDING")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["counsellor", "date", "time"],
                name="unique_appointment_slot"
            )
        ]

    def __str__(self):
        return f"{self.date} {self.time} – {self.full_name} with {self.counsellor}"
