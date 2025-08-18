import hashlib
from django.conf import settings
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.contrib.sessions.models import Session
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.db.models.signals import pre_save, post_save
from django.utils.timezone import now


from .models import User, KnownDevice
from utils.email_notifications import send_account_notification

User = get_user_model()

print("✅ Signals loaded")

# -------------------------
# SESSION SECURITY SIGNALS
# -------------------------

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


# -------------------------
# PROFILE UPDATE SIGNAL (OPTIONAL)
# -------------------------

# Track fields we actually want to monitor
PROFILE_FIELDS = {"first_name", "last_name", "email"}  

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

# -------------------------
# NEW DEVICE DETECTION
# -------------------------

def get_client_ip(request):
    xff = request.META.get('HTTP_X_FORWARDED_FOR')
    return xff.split(',')[0].strip() if xff else request.META.get('REMOTE_ADDR')


def fingerprint_user_agent(request):
    ua = (request.META.get('HTTP_USER_AGENT') or '').strip()
    fp = hashlib.sha256(ua.encode('utf-8')).hexdigest()
    return fp, ua


@receiver(user_logged_in)
def notify_on_new_device(sender, request, user, **kwargs):
    """
    Send an email ONLY when the login comes from a NEW device.
    Track last_seen on every login from the device.
    No emails on logout or repeated logins from known devices.
    """
    ip = get_client_ip(request)
    fp, ua = fingerprint_user_agent(request)

    # Get or create the device
    device, created = KnownDevice.objects.get_or_create(
        user=user,
        fingerprint=fp,
        defaults={'user_agent': ua, 'last_ip': ip}
    )

    # Update last_seen and last_ip for every login
    device.last_seen = timezone.now()
    if device.last_ip != ip:
        device.last_ip = ip
    device.save(update_fields=['last_ip', 'last_seen'])

    # Send email only if this is a NEW device
    if created:
        subject = "New device sign-in to your Hardhat account"
        body = (
            f"Hi {getattr(user, 'first_name', '') or user.username},\n\n"
            "We noticed a sign-in from a new device on your account.\n\n"
            f"Time: {timezone.now():%Y-%m-%d %H:%M:%S %Z}\n"
            f"IP: {ip}\n"
            f"Device: {ua or 'Unknown'}\n\n"
            "If this was you, no action is needed.\n"
            "If not, please reset your password immediately and contact support."
        )
        send_account_notification(user, subject, body)
