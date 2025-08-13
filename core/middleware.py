import logging
from django.utils.timezone import now
from django.shortcuts import redirect

from django.contrib.auth import logout
from django.utils.deprecation import MiddlewareMixin
from django.urls import reverse
from django.utils import translation
logger = logging.getLogger('admin_logout_logger')

class AutoLogoutMiddleware(MiddlewareMixin):
    """
    Middleware to log out users (except superusers) when they leave the admin area.
    """
    def process_request(self, request):
        user = request.user
        if user.is_authenticated:
            is_admin_page = request.path.startswith('/admin')
            if not user.is_superuser:
                if not is_admin_page and request.session.get('admin_session'):
                    logout(request)
                    request.session.pop('admin_session', None)
                    logger.info(f"User {user.username} has been logged out after leaving the admin area.")
                elif is_admin_page:
                    request.session['admin_session'] = True





class LogRequestMiddleware:
    """
    Middleware to log IP address and accessed URL.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Process the request
        response = self.get_response(request)

        # Log the IP and page accessed
        if request.user.is_authenticated:
            session_ip = request.session.get('ip_address')
            session_ua = request.session.get('user_agent')
            session_token = request.session.get('session_token')
            current_ip = self.get_client_ip(request)
            current_ua = request.META.get('HTTP_USER_AGENT')

            # Check for IP address mismatch
            if session_ip and session_ip != current_ip:
                logger.warning(f"Session IP mismatch! Session IP: {session_ip}, Current IP: {current_ip}")
                request.session.flush()
                return redirect('login')  # Redirect to login

            # Check for User-Agent mismatch
            if session_ua and session_ua != current_ua:
                logger.warning(f"Session UA mismatch! Session UA: {session_ua}, Current UA: {current_ua}")
                request.session.flush()
                return redirect('login')

            # Check for session token mismatch
            if session_token and session_token != request.session.session_key:
                logger.warning(f"Session token mismatch! Session token: {session_token}, Current session ID: {request.session.session_key}")
                request.session.flush()
                return redirect('login')

        # Log the IP and accessed URL if no hijacking is detected
        self.log_request(request)

        return response

        # Continue processing the request
        return self.get_response(request)
    


    def log_request(self, request):
        ip = self.get_client_ip(request)
        path = request.path

        # Log the information
        logger.info(f"IP: {ip} accessed {path}")
    def get_client_ip(self, request):
        """
        Extracts client IP address from request headers.
        """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip   


class ForceDefaultLanguageMiddleware:
  
    # Force the default language to English, ignoring the browser Accept-Language
   
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.session.get('django_language'):
            translation.activate('en')
            request.session['django_language'] = 'en'
            request.LANGUAGE_CODE = 'en'
        return self.get_response(request)