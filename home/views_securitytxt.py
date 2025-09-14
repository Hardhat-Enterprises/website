from django.http import HttpResponse
from django.conf import settings

def security_txt(request):
    SECURITY_TXT = f"""Contact: mailto:{getattr(settings, 'SECURITY_EMAIL', 'security@hardhat.com')}
Policy: https://hardhat.com/vulnerability-disclosure
Preferred-Languages: en
Canonical: https://hardhat.com/.well-known/security.txt
Expires: 2026-01-01T00:00:00.000Z
"""
    resp = HttpResponse(SECURITY_TXT, content_type="text/plain; charset=utf-8")
    resp["Cache-Control"] = "public, max-age=86400"
    return resp
