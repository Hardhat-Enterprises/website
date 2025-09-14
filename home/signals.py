from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.contrib.sessions.models import Session
from django.dispatch import receiver
from django.utils.timezone import now
from django.contrib.auth.signals import user_login_failed
from django.core.signals import request_finished
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.db.models.signals import pre_save
from .models import PasswordHistory

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


User = get_user_model()

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