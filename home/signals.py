from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Comment, Notification
from django.contrib.auth.models import User

@receiver(post_save, sender=Comment)
def create_comment_notification(sender, instance, created, **kwargs):
    if created:
        # Create a notification for the post author when a new comment is added
        message = f"{instance.user.username} commented on your post."
        Notification.objects.create(
            user=instance.post.author,  # The user who should receive the notification
            message=message,
            url=f'/posts/{instance.post.id}/'
        )
