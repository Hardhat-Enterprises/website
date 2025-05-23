from django.contrib import admin

from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.urls import path
from django.db.models import Count
from django.db.models.functions import TruncDate
from django.db.models.functions import ExtractWeekDay
import json

from home.models import LeaderBoardTable, Experience,CyberChallenge
from django.contrib.auth import get_user_model
User = get_user_model()

from .models import BlacklistedIP

@admin.register(BlacklistedIP)
class BlacklistedIPAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'is_blacklisted', 'created_at')

@staff_member_required
def admin_statistics_view(request):
    return render(request, "admin/statistics.html", {
        "title": "Statistics"
    })

@staff_member_required
def admin_dashboard(request):
    #Data for first row
    total_users = User.objects.count()
    total_challenges = CyberChallenge.objects.count()
    total_dashboard= LeaderBoardTable.objects.count()
    total_feedback = Experience.objects.count()
   
    #Data for charts
    #For Feedback Receive Within A Week

    data = (
        Experience.objects.annotate(weekday=ExtractWeekDay('created_at'))
        .values('weekday')
        .annotate(count=Count('id'))
        .order_by('weekday')
    )
    # Initialize all days with zero counts
    weekday_map = {1: 'Sunday', 2: 'Monday', 3: 'Tuesday', 4: 'Wednesday',
                   5: 'Thursday', 6: 'Friday', 7: 'Saturday'}
    chart_data = {day: 0 for day in weekday_map.values()}
    for entry in data:
        day_name = weekday_map[entry['weekday']]
        chart_data[day_name] = entry['count']

    feedback_labels = json.dumps(list(chart_data.keys()))
    feedback_data = json.dumps(list(chart_data.values()))

    #For CyberChallenges Chart
    category_counts = CyberChallenge.objects.values('category').annotate(total=Count('id'))
    categories = {
        'network': 0,
        'web': 0,
        'crypto': 0,
        'general': 0,
    }
    for item in category_counts:
        categories[item['category']] = item['total']

    #For User Registrations Over Time Chart
    data = (
        User.objects
        .filter(created_at__isnull=False)
        .annotate(date=TruncDate('created_at'))
        .values('date')
        .annotate(count=Count('id'))
        .order_by('date')
    )

    user_labels = [entry['date'].strftime('%Y-%m-%d') for entry in data]
    user_registration = [entry['count'] for entry in data]

    # return JsonResponse({
    #     'labels': labels,
    #     'data': values,
    # })

    context = {
        "title": "Admin Dashboard",
        "total_users": total_users,
        "total_feedback": total_feedback,
        "total_dashboard": total_dashboard,
        "total_challenges":total_challenges,
        "total_question_in_each_category": categories,
        "user_labels": user_labels,
        "user_registration":user_registration,
        "feedback_labels":feedback_labels,
        "feedback_data":feedback_data
    }
    

    return render(request, "admin/dashboard.html", context)

class CustomAdminSite(admin.AdminSite):
    def get_app_list(self, request, _=None):
        app_list = super().get_app_list(request)
        app_list += [
            {
                "name": "Statistics",
                "app_label": "statistics_app",
                "models": [
                    {
                        "name": "Statistics",
                        "object_name": "statistics",
                        "admin_url": "/admin/statistics",
                        "view_only": True,
                    }
                ],
            },
            {
            "name": "Dashboard",
            "app_label": "dashboard_app",
            "models": [
                {
                    "name": "Admin Dashboard",
                    "object_name": "dashboard",
                    "admin_url": "/admin/dashboard",
                    "view_only": True,
                }
            ],
        }
        ]
        return app_list

    def get_urls(self):
        urls = super().get_urls()
        urls += [
            path("statistics/", admin_statistics_view, name="admin-statistics"),
            path("dashboard/", admin_dashboard, name="admin-dashboard"),
        ]
        return urls