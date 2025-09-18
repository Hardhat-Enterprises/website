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
    print(f"DEBUG: check_deakin_email called - email={email}, user={user}")
    logging.getLogger('social').info(f"check_deakin_email: email={email}, user={user}")
    
    if not email:
        messages.error(None, "Microsoft did not return an email address.")
        raise AuthForbidden('No email address provided')
    
    # Allow ALL @deakin.edu.au emails
    if email.endswith('@deakin.edu.au'):
        # This is a valid Deakin email - continue the pipeline
        logging.getLogger('social').info(f"check_deakin_email: Valid Deakin email {email}, user is {'new' if user is None else 'existing'}")
        print(f"DEBUG: Valid Deakin email {email}, user is {'new' if user is None else 'existing'}")
        return {'is_new': user is None}
    else:
        # Block non-Deakin emails
        logging.getLogger('social').warning(f"check_deakin_email: Rejecting non-Deakin email {email}")
        print(f"DEBUG: Rejecting non-Deakin email {email}")
        messages.error(None, f"Only Deakin University accounts are allowed. Your email ({email}) is not a @deakin.edu.au email.")
        raise AuthForbidden('Only Deakin email addresses are allowed')


def set_oauth_redirect_url(strategy, details, user=None, *args, **kwargs):
    """
    Custom pipeline to ensure OAuth users are redirected to dashboard after authentication.
    This overrides the default get_login_redirect_url behavior for OAuth users.
    """
    import logging
    from django.shortcuts import redirect
    from django.http import HttpResponseRedirect
    
    print(f"DEBUG: set_oauth_redirect_url called - Set redirect to /dashboard/ for user {user}")
    
    # Set the redirect URL to dashboard for OAuth authentication
    strategy.session_set('next', '/dashboard/')
    
    # Also set it in the strategy's redirect_uri
    if hasattr(strategy, 'redirect_uri'):
        strategy.redirect_uri = '/dashboard/'
    
    # Set it in the request session as well
    request = strategy.request
    if request:
        request.session['next'] = '/dashboard/'
        request.session['social_auth_redirect'] = '/dashboard/'
        request.session['redirect_to_dashboard'] = True
        request.session['force_dashboard_redirect'] = True
        print(f"DEBUG: Set session redirect_to_dashboard = True")
        print(f"DEBUG: Set session force_dashboard_redirect = True")
    
    logging.getLogger('social').info(f"set_oauth_redirect_url: Set redirect to /dashboard/ for user {user}")
    
    return {'redirect_uri': '/dashboard/'}


def ensure_user_authenticated(strategy, details, user=None, *args, **kwargs):
    """
    Ensure the user is properly authenticated after OAuth flow.
    This helps prevent redirect back to login page.
    """
    import logging
    from django.utils import timezone
    
    print(f"DEBUG: ensure_user_authenticated called - user: {user}, is_authenticated: {user.is_authenticated if user else 'No user'}")
    
    if user and user.is_authenticated:
        logging.getLogger('social').info(f"ensure_user_authenticated: User {user.email} is properly authenticated")
        print(f"DEBUG: User {user.email} is authenticated")
        
        # Mark user as active and verified if they came through OAuth
        if not user.is_active:
            user.is_active = True
        if not user.is_verified:
            user.is_verified = True
        
        # Update last activity to prevent timeout middleware from logging out
        user.last_activity = timezone.now()
        user.save(update_fields=['is_active', 'is_verified', 'last_activity'])
        
        # Set session information to prevent hijacking middleware from redirecting
        request = strategy.request
        if request:
            # Get client IP address
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0]
            else:
                ip = request.META.get('REMOTE_ADDR')
            
            request.session['ip_address'] = ip
            request.session['user_agent'] = request.META.get('HTTP_USER_AGENT', '')
            request.session['session_token'] = request.session.session_key
            request.session['last_activity'] = timezone.now().timestamp()
            
            # Set OAuth authentication flag
            request.session['oauth_authenticated'] = True
            
            # FORCE redirect to dashboard
            request.session['next'] = '/dashboard/'
            request.session['social_auth_redirect'] = '/dashboard/'
            request.session['redirect_to_dashboard'] = True
            request.session['force_dashboard_redirect'] = True
            
            logging.getLogger('social').info(f"ensure_user_authenticated: Set session info for user {user.email}")
            print(f"DEBUG: Set session info for user {user.email}")
            print(f"DEBUG: Set oauth_authenticated flag to True")
            print(f"DEBUG: FORCED redirect to dashboard in session")
    else:
        logging.getLogger('social').warning("ensure_user_authenticated: User authentication failed")
        print(f"DEBUG: User authentication failed - user: {user}")
    
    return None

