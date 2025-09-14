import hashlib
from django.conf import settings
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.contrib.auth import get_user_model
from django.contrib.sessions.models import Session
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.db.models.signals import pre_save, post_save
from django.utils.timezone import now
from django_user_agents.utils import get_user_agent
import logging
from .models import UserDevice


from .models import User, UserDevice
from utils.email_notifications import send_account_notification
from utils.device_fingerprint import generate_device_fingerprint

logger = logging.getLogger(__name__)
User = get_user_model()

print("✅ Signals loaded")


# SESSION SECURITY SIGNALS
@receiver(user_logged_in)
def set_session_last_activity_on_login(sender, request, user, **kwargs):
    """
    Set the initial 'last_activity' in session on user login.
    Prevent concurrent sessions by deleting the old one.
    """
    request.session['last_activity'] = timezone.now().timestamp()

    if not request.session.session_key:
        request.session.save()

    current_session_key = request.session.session_key
    print(f"[Login] Current session key: {current_session_key}")

    if hasattr(user, 'current_session_key') and user.current_session_key and user.current_session_key != current_session_key:
        try:
            old_session = Session.objects.get(session_key=user.current_session_key)
            old_session.delete()
            print(f"[Login] Deleted old session: {user.current_session_key}")
        except Session.DoesNotExist:
            print("[Login] Old session not found.")

    user.current_session_key = current_session_key
    user.save(update_fields=['current_session_key'])

# DEVICE RECOGNITION SIGNAL
@receiver(user_logged_in)
def track_login(sender, request, user, **kwargs):
    # Get IP address from request
    ip = request.META.get("REMOTE_ADDR", "")
    # Get user agent string
    user_agent = request.META.get("HTTP_USER_AGENT", "")
    # Create a device fingerprint
    device_fp = generate_device_fingerprint(user_agent, ip)
    # Simple readable device info
    device_info = user_agent.split(")")[0] if user_agent else "Unknown device"
    print(f"Login from {ip}, device: {device_info}") #DEBUG

    # Look for existing device
    device, created = UserDevice.objects.get_or_create(
        user=user,
        device_name=device_info,
        ip_address=ip,
        defaults={"last_seen": timezone.now()},
    )
    print(f"Device created? {created}") #DEBUG

    if created:
        print("Sending email notification...") #DEBUG
        # Notify only on *new* devices
        message = f"A login to your account was detected from {ip} using {device_info}."
        send_account_notification(user=user, subject="New Login to Your HardHat Account", message=message)
    else:
        # Update last_seen timestamp
        device.last_seen = timezone.now()
        device.save(update_fields=["last_seen"])



@receiver(user_logged_out)
def clear_session_last_activity_on_logout(sender, request, user, **kwargs):
    """
    Clear the 'last_activity' session key on user logout.
    """
    if 'last_activity' in request.session:
        del request.session['last_activity']

    if hasattr(user, 'current_session_key') and user.current_session_key == request.session.session_key:
        user.current_session_key = None
        user.save(update_fields=['current_session_key'])


# PROFILE UPDATE SIGNAL
# Track fields we actually want to monitor
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


