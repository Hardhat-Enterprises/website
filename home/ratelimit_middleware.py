from django.core.cache import cache
from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.utils import timezone

class GlobalLockoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the global lockout is active
        if cache.get('global_lockout'):
            # Render a custom 403 Forbidden page
            return self.render_forbidden_page(request)
        
        # Process the request and get the response
        response = self.get_response(request)
        return response

    def render_forbidden_page(self, request):
        # Calculate remaining time for the lockout
        wait_time = 60  # seconds
        lockout_start_time = cache.get('lockout_start_time', timezone.now())
        remaining_time = wait_time - (timezone.now() - lockout_start_time).total_seconds()
        remaining_time = max(0, remaining_time)  # Ensure it's not negative

        # Render your custom forbidden page template with countdown
        return render(request, 'accounts/rate_limit_exceeded.html', {
            'message': 'Access denied due to too many login attempts. Please try again later.',
            'wait_time': remaining_time,
        }, status=403)