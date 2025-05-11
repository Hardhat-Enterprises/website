from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import Count, Avg
from .models import UserActivity

@csrf_exempt
def log_event(request):
    if request.method == "POST":
        data = request.POST
        UserActivity.objects.create(
            session_key=request.session.session_key or 'anonymous',
            page_url=data.get("page_url"),
            event_type=data.get("event_type"),
            element_id=data.get("element_id"),
            scroll_depth=data.get("scroll_depth") or None,
            duration=data.get("duration") or None
        )
        return JsonResponse({"status": "success"})
    return JsonResponse({"status": "fail"})

def analytics_dashboard(request):
    # Top clicked elements
    top_clicks = (
        UserActivity.objects.filter(event_type="click")
        .values("element_id")
        .annotate(count=Count("id"))
        .order_by("-count")[:10]
    )

    # Top visited pages
    top_pages = (
        UserActivity.objects
        .values("page_url")
        .annotate(count=Count("id"))
        .order_by("-count")[:10]
    )

    # Averages
    avg_scroll = UserActivity.objects.aggregate(Avg("scroll_depth"))["scroll_depth__avg"]
    avg_duration = UserActivity.objects.aggregate(Avg("duration"))["duration__avg"]

    return render(request, "tracker/analytics.html", {
        "top_clicks": top_clicks,
        "top_pages": top_pages,
        "avg_scroll": round(avg_scroll or 0, 1),
        "avg_duration": round(avg_duration or 0, 1),
    })
