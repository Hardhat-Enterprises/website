from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from django.utils.timezone import now
 
@receiver(user_logged_in)
def set_session_last_activity_on_login(sender, request, user, **kwargs):
    """
    Set the initial 'last_activity' in session on user login.
    """
    request.session['last_activity'] = now().timestamp()
 
@receiver(user_logged_out)
def clear_session_last_activity_on_logout(sender, request, user, **kwargs):
    """
    Clear the 'last_activity' session key on user logout.
    """
    if 'last_activity' in request.session:
        del request.session['last_activity']