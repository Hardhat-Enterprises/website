import logging
from django.utils.timezone import now
from django.shortcuts import redirect

logger = logging.getLogger('page_access_logger')

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
        ip = self.get_client_ip(request)
        path = request.path

        # Log the information
        logger.info(f"IP: {ip} accessed {path}")