from .models import VisitorLog
from django.utils.deprecation import MiddlewareMixin

class VisitorLogMiddleware(MiddlewareMixin):
    def process_request(self, request):
        ip_address = self.get_client_ip(request)
        user = request.user if request.user.is_authenticated else None
        page_url = request.build_absolute_uri()

        VisitorLog.objects.create(
            ip_address=ip_address,
            user=user,
            page_url=page_url
        )

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
