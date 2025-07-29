from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.contrib.sessions.models import Session
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now
from .models import User
from django.contrib.auth.signals import user_login_failed
from django.core.signals import request_finished
from utils.email_notifications import send_account_notification
from django.contrib.auth import get_user_model


User = get_user_model()


@receiver(user_logged_in)
def set_session_last_activity_on_login(sender, request, user, **kwargs):
    """
    Set the initial 'last_activity' in session on user login.
    """
    request.session['last_activity'] = now().timestamp()

    # Force session save if no session key available
    if not request.session.session_key:
        request.session.save()

    current_session_key = request.session.session_key
    print(f"[Login] Current session key: {current_session_key}")

    # Prevent concurrent logins
    if hasattr(user, 'current_session_key') and user.current_session_key and user.current_session_key != current_session_key:
        try:
            old_session = Session.objects.get(session_key=user.current_session_key)
            old_session.delete()
            print(f"[Login] Deleted old session: {user.current_session_key}")
        except Session.DoesNotExist:
            print("[Login] Old session not found.")

    # Save new session key to user model
    user.current_session_key = current_session_key
    user.save()

    # Send login email notification
    ip = request.META.get('REMOTE_ADDR')
    browser = request.META.get('HTTP_USER_AGENT', 'Unknown Browser')
    message = f"You logged in on {now()} from IP: {ip}\nBrowser: {browser}"
    send_account_notification(user, "New Login Detected", message)
 
@receiver(user_logged_out)
def clear_session_last_activity_on_logout(sender, request, user, **kwargs):
    """
    Clear the 'last_activity' session key on user logout.
    """
    if 'last_activity' in request.session:
        del request.session['last_activity']

    # Clear session tracking on logout
    if hasattr(user, 'current_session_key') and user.current_session_key == request.session.session_key:
        user.current_session_key = None
        user.save()

    # Send logout email notification
    ip = request.META.get('REMOTE_ADDR')
    message = f"You logged out on {now()} from IP: {ip}"
    send_account_notification(user, "Account Logout Notification", message)

def clear_user_sessions(user, current_session_key=None):
    """
    Clear all sessions for a user except the current one
    """
    if not user:
        return

    # Get all sessions for user
    sessions = Session.objects.filter(expire_date__gte=now())
    if current_session_key:
        sessions = sessions.exclude(session_key=current_session_key)
    
    for session in sessions:
        session_data = session.get_decoded()
        if str(user.id) == session_data.get('_auth_user_id'):
            session.delete()


@receiver(post_save, sender=User)
def notify_user_profile_update(sender, instance, created, **kwargs):
    """
    Send email notification when the user updates their profile.
    """
    if not created:  # Only send on updates, not when a new user is created
        message = f"Your profile was updated on {now()}.\n\nIf this wasn't you, please secure your account immediately."
        send_account_notification(instance, "Profile Update Notification", message)