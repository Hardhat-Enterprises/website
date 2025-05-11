from django.utils.deprecation import MiddlewareMixin

class NoAdminCacheMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        if request.path.startswith('/admin/'):
            response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
            response['Pragma'] = 'no-cache'
            response['Expires'] = '0'
        return response
