from django.core.mail import send_mail
from django.conf import settings

def send_account_notification(user, subject, message):
    """
    Sends a notification email to the given user.
    """
    if not user.email:
        return False  # No email on user account

    full_message = f"""
Hi {user.first_name or user.username},

{message}

If this wasn't you, please check your account security immediately.

Thanks,
HardHat Website Team
    """
    return send_mail(
        subject=subject,
        message=full_message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user.email],
        fail_silently=False,
    )
