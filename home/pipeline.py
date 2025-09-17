"""
Custom pipeline functions for social authentication.
"""

from django.contrib import messages
from django.shortcuts import redirect
from social_core.exceptions import AuthForbidden


def check_deakin_email(strategy, details, user=None, *args, **kwargs):
    """
    Custom pipeline to restrict Microsoft authentication to Deakin University emails.
    FIXED: Now properly allows all Deakin emails and supports user creation.
    """
    import logging
    
    email = details.get('email', '').lower()
    logging.getLogger('social').debug(f"check_deakin_email: email={email}, user={user}")
    
    if not email:
        messages.error(None, "Microsoft did not return an email address.")
        raise AuthForbidden('No email address provided')
    
    # Allow ALL @deakin.edu.au emails
    if email.endswith('@deakin.edu.au'):
        # This is a valid Deakin email - continue the pipeline
        logging.getLogger('social').debug(f"check_deakin_email: Valid Deakin email {email}, user is {'new' if user is None else 'existing'}")
        return {'is_new': user is None}
    else:
        # Block non-Deakin emails
        logging.getLogger('social').debug(f"check_deakin_email: Rejecting non-Deakin email {email}")
        messages.error(None, f"Only Deakin University accounts are allowed. Your email ({email}) is not a @deakin.edu.au email.")
        raise AuthForbidden('Only Deakin email addresses are allowed')

