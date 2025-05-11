from django.db import models

class UserActivity(models.Model):
    session_key = models.CharField(max_length=100)
    page_url = models.URLField()
    event_type = models.CharField(max_length=50)
    element_id = models.CharField(max_length=100, blank=True, null=True)
    scroll_depth = models.IntegerField(blank=True, null=True)
    duration = models.FloatField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.event_type} @ {self.page_url}"