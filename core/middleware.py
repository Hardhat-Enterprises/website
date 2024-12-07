import logging
from django.utils.timezone import now

logger = logging.getLogger('custom_logger')

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
        ip = self.get_client_ip(request)
        # Get the accessed page
        path = request.path

        # Log the information
        logger.info(f"IP: {ip} accessed {path}")

    def get_client_ip(self, request):
        """
        Retrieve the IP address from the request object.
        """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR', 'Unknown')
        return ip
