import logging
from django.utils.timezone import now
from django.shortcuts import redirect

logger = logging.getLogger('page_access_logger')

class LogRequestMiddleware:
    """
    Middleware to log IP address and accessed URL,
    and prevent session hijacking by checking IP, User-Agent, and session ID.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Log the request
        self.log_request(request)

        if request.user.is_authenticated:
            session_ip = request.session.get('ip_address')
            session_ua = request.session.get('user_agent')
            session_token = request.session.get('session_token')
            current_ip = self.get_client_ip(request)
            current_ua = request.META.get('HTTP_USER_AGENT')

            if session_ip and session_ip != current_ip:
                logger.warning(f"Session IP mismatch! Session IP: {session_ip}, Current IP: {current_ip}")
                request.session.flush()
                return redirect('login')  # Redirect to login

            if session_ua and session_ua != current_ua:
                logger.warning(f"Session UA mismatch! Session UA: {session_ua}, Current UA: {current_ua}")
                request.session.flush()
                return redirect('login')

            if session_token and session_token != request.session.session_key:
                logger.warning(f"Session token mismatch! Session token: {session_token}, Current session ID: {request.session.session_key}")
                request.session.flush()
                return redirect('login')

        return self.get_response(request)

    def log_request(self, request):
        ip = self.get_client_ip(request)
        path = request.path
        logger.info(f"{now()} - IP: {ip} accessed {path}")

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')