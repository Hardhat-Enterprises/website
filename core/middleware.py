class SecurityHeadersMiddleware:
    """
    Middleware to add security headers that help mitigate vulnerabilities
    in third-party JavaScript libraries and prevent common attacks.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response['Content-Security-Policy'] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data: https:; "
            "font-src 'self' https:; "
            "connect-src 'self'; "
            "frame-ancestors 'none'; "
            "base-uri 'self';"
        )
        response['X-Frame-Options'] = 'DENY'
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        response['Permissions-Policy'] = (
            'geolocation=(), '
            'microphone=(), '
            'camera=(), '
            'payment=(), '
            'usb=(), '
            'magnetometer=(), '
            'accelerometer=(), '
            'gyroscope=()'
        )
        return response

class HoneypotMiddleware:
    """
    Middleware to detect and log requests to honeypot (fake) paths.
    Normal users will never visit these paths.
    If triggered, log the attempt and return a 404 page.
    """
    HONEYPOT_PATHS = [
        "/admin-secret",
        "/Main-admin",
        "/superuser",
        "/dashboard-old",
        "/backup.sql",
        "/db.dump",
        "/config.php",
        "/env.bak",
        "/administration-login",
        "/auth-test",
        "/secure-login",
        "/test-page",
        "/debug/",
        "/old-site/"
    ]

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path
        if path in self.HONEYPOT_PATHS:
            ip = self.get_client_ip(request)
            ua = request.META.get("HTTP_USER_AGENT", "unknown")
            Honeypot_logger.warning(
                f"HONEYPOT TRIGGERED: Path={path}, IP={ip}, User-Agent={ua}"
            )
            return render(request, "404.html", status=404)
        return self.get_response(request)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR", "")
        return ip