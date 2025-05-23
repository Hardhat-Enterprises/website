from django.contrib.admin import AdminSite
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.urls import path


@staff_member_required
def admin_statistics_view(request):
    return render(request, "admin/statistics.html", {
        "title": "Statistics"
    })


class CustomAdminSite(AdminSite):
    site_header = "HardHat Admin"
    site_title = "HardHat Admin Portal"
    index_title = "Welcome to HardHat Enterprise Admin Panel"

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
            }
        ]
        return app_list

    def get_urls(self):
        urls = super().get_urls()
        urls += [
            path("statistics/", admin_statistics_view, name="admin-statistics"),
        ]
        return urls
