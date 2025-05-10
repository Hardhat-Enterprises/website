import datetime
import time
from django.conf import settings
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.utils.timezone import now, make_aware

# Idle timeout middleware has been rewritten as Logout middleware to allow persistence of sessions. 
 
# class IdleTimeoutMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response
 
#     def __call__(self, request):
#         # If user is authenticated, updates the last_activity field to the time of last get or post message
#         if request.user.is_authenticated:
#             request.user.last_activity = now()
#             request.user.save(update_fields=["last_activity"])
#             return self.get_response(request)
 
#         # Get current time and last activity from the session
#         current_time = now()
#         last_activity_timestamp = (request.session.get('last_activity', current_time.timestamp()))
#         last_activity_time = make_aware(datetime.datetime.fromtimestamp(last_activity_timestamp))
 
#         # Calculate idle time in seconds
#         idle_time = (current_time - last_activity_time).total_seconds()
 
#         # If idle time exceeds session timeout, log out the user
#         if idle_time > settings.SESSION_COOKIE_AGE:
#             logout(request)
#             return redirect('login')
 
#         # Update the session with the current activity timestamp
#         request.session['last_activity'] = current_time.timestamp()
#         return self.get_response(request)

class LogoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # If user is authenticated, updates the last_activity field to the time of last get or post message
        if request.user.is_authenticated:
            now = time.time()
            last_activity = request.session.get('last_activity', now)
            
            # 10 minutes = 600 seconds
            if now - last_activity > 600:
                request.session['logged_out_for_inactivity'] = True
                request.session.cycle_key()  # Safe: rotates session ID
                request.session.pop('_auth_user_id', None)
                request.session.pop('_auth_user_backend', None)
                request.session.pop('_auth_user_hash', None)
                return redirect('login')
            else:
                request.session['last_activity'] = now
        return self.get_response(request)

