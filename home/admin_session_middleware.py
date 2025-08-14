#created by Bryce Bacon 11/08/2025 brycedbacon@gmail.com

import logging
from django.utils.timezone import now
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.utils.deprecation import MiddlewareMixin
from django.contrib import messages
from django.urls import reverse
from django.core.cache import cache

logger = logging.getLogger('audit_logger')

class AdminSessionMiddleware(MiddlewareMixin):
    
    #verify the admin session
    def admin_session(self, request):
        user = request.user

        #check of admin or staff priviledges 
        if not user.is_staff and not user.is_superuser:
            return False
        
        #check if the session is valid
        if not request.session.get('admin_session', False):
            return False
        
        #check for admin session exsists
        admin_session_id = request.session.get('admin_session_id')
        if admin_session_id:
            try:
                from .models import AdminSession
                admin_session = AdminSession.objects.get(
                    id=admin_session_id,
                    user=user,
                    is_active=True,
                    expires_at__gt=now()
                )
                return True
            except AdminSession.DoesNotExist:
                return False
            
        return False
    
    #check if admin session has expired. 
    def is_admin_session_expired(self, request):
        admin_login_time = request.session.get('admin_login_time')
        if not admin_login_time:
            return False
        
        admin_session_id = request.session.get('admin_session_id')
        if admin_session_id:
            try:
                from .models import AdminSession
                admin_session = AdminSession.objects.get(id=admin_session_id)
                return admin_session.is_expired(timeout_minutes=30)
            except AdminSession.DoesNotExist:
                return True

        return True
    
    def validate_admin_session_sec(self, request):
        session_ip = request.session.get('ip_address')
        current_ip = self.get_client_ip(request)

        if session_ip and session_ip != current_ip:
            logger.warning(f"Admin session IP mismatch: {session_ip} vs {current_ip}")
            return False

        # Check the user agent
        session_ua = request.session.get('user_agent')
        current_ua = request.META.get('HTTP_USER_AGENT', '')

        if session_ua and session_ua != current_ua:
            logger.warning(f"Admin session User-Agent mismatch")
            return False

        return True
    
    def terminate_admin_session(self, request, reason):
        #terminate the admin session
        user = request.user

        # Mark admin session as logged out
        admin_session_id = request.session.get('admin_session_id')
        if admin_session_id:
            try:
                from .models import AdminSession
                admin_session = AdminSession.objects.get(id=admin_session_id)
                admin_session.mark_logout(reason=reason)
            except AdminSession.DoesNotExist:
                pass

        # Log the session termination
        logger.warning(f"Admin session terminated for {user.email} - Reason: {reason}")

        # Clear session and logout
        request.session.flush()
        logout(request)

        # Set appropriate message based on reason
        if reason == 'timeout':
            messages.warning(request, 'Your admin session has expired due to inactivity. Please log in again.')
        elif reason == 'security_violation':
            messages.error(request, 'Your admin session was terminated due to security concerns. Please log in again.')
        else:
            messages.info(request, 'Your admin session has ended. Please log in again.')

        return redirect('admin_login')

    def get_client_ip(self, request):
        #ai generated code
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    #This is middleware to manage admin/staff sessions
    def process_request(self, request):
        user = request.user

        if not user.is_authenticated:
            return None
        
        admin_session = request.session.get('admin_session', False)
#admin security checks
        if admin_session:
            if not self.admin_session(request):
                return self.terminate_admin_session(request, 'security_violation')
        
            if self.is_admin_session_expired(request):
                return self.terminate_admin_session(request, 'session_expired')
        
            # Update admin session activity
            admin_session_id = request.session.get('admin_session_id')
            if admin_session_id:
                try:
                    from .models import AdminSession
                    admin_session = AdminSession.objects.get(id=admin_session_id)
                    admin_session.update_last_activity()
                except AdminSession.DoesNotExist:
                    pass

        if not self.validate_admin_session_sec(request):
            return self.terminate_admin_session(request, 'session_state_invalid')
        
        return None
    
