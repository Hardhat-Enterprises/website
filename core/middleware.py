import logging
from django.utils.timezone import now

from django.contrib.auth import logout
from django.utils.deprecation import MiddlewareMixin
from django.urls import reverse
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
        self.log_request(request)

        return response

    def log_request(self, request):
        # Get the IP address from the request
        ip = request.get_host()
        # Get the accessed page
        path = request.path

        # Log the information
        logger.info(f"IP: {ip} accessed {path}")