import logging
from django.utils.timezone import now

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
        # Get the IP address from the request
        ip = request.get_host()
        # Get the accessed page
        path = request.path

        # Log the information
        logger.info(f"IP: {ip} accessed {path}")