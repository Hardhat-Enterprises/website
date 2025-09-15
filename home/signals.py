import logging
from django.utils.timezone import now
from django.contrib.auth import get_user_model
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django_user_agents.utils import get_user_agent

from .models import PasswordHistory, UserDevice
from utils.email_notifications import send_account_notification
from utils.device_fingerprint import generate_device_fingerprint

logger = logging.getLogger(__name__)
User = get_user_model()

# =====================================================
# PROFILE UPDATE SIGNAL
# Track only the fields we want to monitor
# =====================================================
PROFILE_FIELDS = {
    "first_name",
    "last_name",
    "email",
    "description",
    "contact_information",
    "connect_with_me",
}

@receiver(pre_save, sender=User)
def cache_old_user(sender, instance, **kwargs):
    """Cache old user before saving, to compare changes."""
    if instance.pk:
        try:
            instance._old_user = User.objects.get(pk=instance.pk)
        except User.DoesNotExist:
            instance._old_user = None

@receiver(post_save, sender=User)
def notify_user_profile_update(sender, instance, created, **kwargs):
    """Notify user when monitored profile fields are updated."""
    if created or not hasattr(instance, "_old_user") or not instance._old_user:
        return

    # Compare only monitored fields
    changed = [
        field for field in PROFILE_FIELDS
        if getattr(instance, field) != getattr(instance._old_user, field)
    ]

    if not changed:
        return  # No real profile changes

    message = (
        f"Your profile was updated on {now()}.\n\n"
        "If this wasn't you, please secure your account immediately."
    )
    send_account_notification(instance, "Profile Update Notification", message)


# =====================================================
# PASSWORD HISTORY SIGNALS
# Keep track of password changes
# =====================================================
@receiver(post_save, sender=User)
def add_initial_password_to_history(sender, instance, created, **kwargs):
    """Store the first password when the user is created."""
    if not created:
        return
    encoded = getattr(instance, "password", "")
    if encoded.strip():
        PasswordHistory.objects.create(user=instance, encoded_password=encoded)

@receiver(pre_save, sender=User)
def store_old_password_before_change(sender, instance, **kwargs):
    """Save the old password before a change, keeping last N entries."""
    if not instance.pk:
        return

    try:
        old = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        return

    old_encoded = (old.password or "").strip()
    new_encoded = (instance.password or "").strip()

    # Only store if password actually changed
    if old_encoded and new_encoded and old_encoded != new_encoded:
        PasswordHistory.objects.create(user=instance, encoded_password=old_encoded)

        KEEP_LAST = 2
        ids_to_keep = list(
            PasswordHistory.objects.filter(user=instance)
            .order_by("-created_at")
            .values_list("id", flat=True)[:KEEP_LAST]
        )
        PasswordHistory.objects.filter(user=instance).exclude(id__in=ids_to_keep).delete()
