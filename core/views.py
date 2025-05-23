from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from home.models import FailedLoginAttempt
from core.models import BlacklistedIP

@staff_member_required
def blacklisted_ips_view(request):
    blacklisted_ips = BlacklistedIP.objects.all()
    failed_logins = FailedLoginAttempt.objects.order_by('-timestamp')[:20]
    return render(request, 'core/admin_dashboard.html', {
        'blacklisted_ips': blacklisted_ips,
        'failed_logins': failed_logins,
    })