import logging
from django.utils.timezone import now

from django.contrib.auth import logout
from django.utils.deprecation import MiddlewareMixin
from django.urls import reverse
logger = logging.getLogger('admin_logout_logger')

class AutoLogoutMiddleware(MiddlewareMixin):
    """
    Middleware to log out the user as soon as they leave the admin page.
    """
    def process_request(self, request):
        user = request.user
        # Only process if the user is logged in
        if user.is_authenticated:
            # Check if the user is currently on the admin page
            is_admin_page = request.path.startswith(reverse('admin:index'))

            # If the user is no longer on the admin page, log them out immediately
            if not is_admin_page:
                logout(request)
                logger.info(f"User {user.get_username()} has been logged out as they left the admin site.")





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