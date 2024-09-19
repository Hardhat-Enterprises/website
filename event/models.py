from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()

class VisitorLog(models.Model):
    ip_address = models.GenericIPAddressField(verbose_name='Visitor IP Address')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Visitor User')
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Visit Time')
    page_url = models.URLField(max_length=200, verbose_name='Visited Page')

    class Meta:
        verbose_name = 'Visitor Log'
        verbose_name_plural = 'Visitor Logs'
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.ip_address} - {self.page_url} - {self.timestamp}"


class UserClickEvent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User', null=True, blank=True)
    page_url = models.URLField(max_length=200, verbose_name='Page')
    clicked_element = models.CharField(max_length=255, verbose_name='Clicked Element')
    click_time = models.DateTimeField(auto_now_add=True, verbose_name='Click Time')

    class Meta:
        verbose_name = 'User Click Event'
        verbose_name_plural = 'User Click Events'
        ordering = ['-click_time']

    def __str__(self):
        return f"{self.user} - {self.clicked_element} - {self.click_time}"
