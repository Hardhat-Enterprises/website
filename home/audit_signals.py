import logging
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from django.utils.timezone import now

audit_logger = logging.getLogger('audit_logger')

#A list to keep track of recent deletions for bulk delete detection
recent_deletes = []

#Trigger before any model instance is saved (created or updated)
@receiver(pre_save)
def log_pre_save(sender, instance, **kwargs):
    # Skip Django internal models to avoid unnecessary logs
    if sender._meta.app_label in ['sessions', 'admin', 'contenttypes', 'auth']:
        return

    # Determine action - CREATE if instance has no primary key, else UPDATE
    action = "UPDATE" if instance.pk else "CREATE"

    # Log the action with full data and timestamp
    audit_logger.info(
        f"[{action}] {sender.__name__} at {now()} | ID: {instance.pk} | Data: {instance.__dict__}"
    )

    #Detect Unusual Activity - Superuser or Staff status changed
    if sender.__name__ == "User" and instance.pk:
        from home.models import User  
        try:
            old_instance = User.objects.get(pk=instance.pk)

            if old_instance.is_superuser != instance.is_superuser:
                audit_logger.warning(
                    f"[ALERT] Superuser status changed for User ID {instance.pk} at {now()} | "
                    f"From {old_instance.is_superuser} → {instance.is_superuser}"
                )

            if old_instance.is_staff != instance.is_staff:
                audit_logger.warning(
                    f"[ALERT] Staff status changed for User ID {instance.pk} at {now()} | "
                    f"From {old_instance.is_staff} → {instance.is_staff}"
                )

        except User.DoesNotExist:
            pass


# Trigger after any model instance is deleted
@receiver(post_delete)
def log_post_delete(sender, instance, **kwargs):
    # Skip internal models
    if sender._meta.app_label in ['sessions', 'admin', 'contenttypes', 'auth']:
        return

    # Record the deletion
    timestamp = now()
    audit_logger.warning(
        f"[DELETE] {sender.__name__} at {timestamp} | ID: {instance.pk} | Data: {instance.__dict__}"
    )

    #Detect Unusual Activity - Bulk Deletions (3+ within 10 seconds)
    recent_deletes.append(timestamp)

    # Keep only the last 10 seconds of deletions
    recent_deletes[:] = [t for t in recent_deletes if (timestamp - t).seconds < 10]

    # Alert if more than three deletions happened in the last 10 seconds
    if len(recent_deletes) >= 3:
        audit_logger.warning(
            f"[ALERT] Potential BULK DELETE detected — {len(recent_deletes)} within 10 seconds!"
        )
