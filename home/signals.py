import hashlib
import logging

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.contrib.sessions.models import Session
from django.core.signals import request_finished
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.timezone import now
from django_user_agents.utils import get_user_agent

from .models import PasswordHistory, UserDevice
from utils.email_notifications import send_account_notification
from utils.device_fingerprint import generate_device_fingerprint

logger = logging.getLogger(__name__)
User = get_user_model()

print("✅ Signals loaded")


# =========================
# SESSION SECURITY SIGNALS
# =========================
@receiver(user_logged_in)
def set_session_last_activity_on_login(sender, request, user, **kwargs):
    """
    Set the initial 'last_activity' in session on user login.
    """
    request.session['last_activity'] = timezone.now().timestamp()

    # Force session save if no session key available
    if not request.session.session_key:
        request.session.save()

    current_session_key = request.session.session_key
    logger.info(f"[Login] Current session key: {current_session_key}")

    # Prevent concurrent logins
    if hasattr(user, 'current_session_key') and user.current_session_key and user.current_session_key != current_session_key:
        try:
            old_session = Session.objects.get(session_key=user.current_session_key)
            old_session.delete()
            logger.info(f"[Login] Deleted old session: {user.current_session_key}")
        except Session.DoesNotExist:
            logger.warning("[Login] Old session not found.")

    # Save new session key to user model
    user.current_session_key = current_session_key
    user.save()


# =========================
# DEVICE RECOGNITION SIGNAL
# =========================
@receiver(user_logged_in)
def track_login(sender, request, user, **kwargs):
    ip = request.META.get("REMOTE_ADDR", "")
    user_agent = request.META.get("HTTP_USER_AGENT", "")
    device_fp = generate_device_fingerprint(user_agent, ip)
    device_info = user_agent.split(")")[0] if user_agent else "Unknown device"
    logger.info(f"Login from {ip}, device: {device_info}")

    device, created = UserDevice.objects.get_or_create(
        user=user,
        device_name=device_info,
        ip_address=ip,
        defaults={"last_seen": timezone.now()},
    )

    if created:
        logger.info("New device detected, sending email notification...")
        message = f"A login to your account was detected from {ip} using {device_info}."
        send_account_notification(user=user, subject="New Login to Your HardHat Account", message=message)
    else:
        device.last_seen = timezone.now()
        device.save(update_fields=["last_seen"])


@receiver(user_logged_out)
def clear_session_last_activity_on_logout(sender, request, user, **kwargs):
    if 'last_activity' in request.session:
        del request.session['last_activity']

    if hasattr(user, 'current_session_key') and user.current_session_key == request.session.session_key:
        user.current_session_key = None
        user.save()


def clear_user_sessions(user, current_session_key=None):
    if not user:
        return

    sessions = Session.objects.filter(expire_date__gte=now())
    if current_session_key:
        sessions = sessions.exclude(session_key=current_session_key)
    for session in sessions:
        session_data = session.get_decoded()
        if str(user.id) == session_data.get('_auth_user_id'):
            session.delete()


# =========================
# PROFILE UPDATE SIGNAL
# =========================
PROFILE_FIELDS = {"first_name", "last_name", "email", "description", "contact_information", "connect_with_me"}  

@receiver(pre_save, sender=User)
def cache_old_user(sender, instance, **kwargs):
    if instance.pk:
        try:
            instance._old_user = User.objects.get(pk=instance.pk)
        except User.DoesNotExist:
            instance._old_user = None


@receiver(post_save, sender=User)
def notify_user_profile_update(sender, instance, created, **kwargs):
    if created or not hasattr(instance, "_old_user") or not instance._old_user:
        return

    changed = [
        field for field in PROFILE_FIELDS
        if getattr(instance, field) != getattr(instance._old_user, field)
    ]

    if not changed:
        return

    message = (
        f"Your profile was updated on {now()}.\n\n"
        "If this wasn't you, please secure your account immediately."
    )
    send_account_notification(instance, "Profile Update Notification", message)


# =========================
# PASSWORD HISTORY SIGNALS
# =========================
@receiver(post_save, sender=User)
def add_initial_password_to_history(sender, instance, created, **kwargs):
    if not created:
        return
    encoded = getattr(instance, "password", "")
    if encoded.strip():
        PasswordHistory.objects.create(user=instance, encoded_password=encoded)


@receiver(pre_save, sender=User)
def store_old_password_before_change(sender, instance, **kwargs):
    if not instance.pk:
        return

    try:
        old = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        return

    old_encoded = (old.password or "").strip()
    new_encoded = (instance.password or "").strip()

    if old_encoded and new_encoded and old_encoded != new_encoded:
        PasswordHistory.objects.create(user=instance, encoded_password=old_encoded)

        KEEP_LAST = 2
        ids_to_keep = list(
            PasswordHistory.objects.filter(user=instance)
            .order_by("-created_at")
            .values_list("id", flat=True)[:KEEP_LAST]
        )
        PasswordHistory.objects.filter(user=instance).exclude(id__in=ids_to_keep).delete()
