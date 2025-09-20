# home/views_robotstxt.py
from django.http import HttpResponse

ROBOTS_TXT = """User-agent: *
Allow: /

# Disallow admin & auth flows
Disallow: /admin/
Disallow: /accounts/
Disallow: /accounts/login/
Disallow: /accounts/signup/

# Crawl budget: skip noisy endpoints
Disallow: /search/suggestions/
Disallow: /api-analytics/

# (Optional) point crawlers to sitemap if available
Sitemap: {sitemap_url}
"""

def robots_txt(request):
    # Build an absolute sitemap URL (works even if /sitemap.xml doesn’t exist yet)
    sitemap_url = request.build_absolute_uri("/sitemap.xml")
    body = ROBOTS_TXT.format(sitemap_url=sitemap_url)
    resp = HttpResponse(body, content_type="text/plain; charset=utf-8")
    resp["Cache-Control"] = "public, max-age=3600"
    return resp
