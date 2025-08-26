# home/templatetags/breadcrumbs.py
from dataclasses import dataclass
from typing import List, Optional, Dict
from django import template
from django.urls import reverse, NoReverseMatch

register = template.Library()

@dataclass
class Crumb:
    label: str
    url: Optional[str] = None  # None = current page (no link)

def _safe_reverse(name: str) -> Optional[str]:
    try:
        return reverse(name)
    except NoReverseMatch:
        return None
    except Exception:
        return None

def _pretty_from_view(view_name: str) -> str:
    """Turn 'pen-testing' -> 'Pen Testing', 'post_detail' -> 'Post Detail'."""
    if not view_name:
        return "Current"
    tail = view_name.split(":")[-1]
    tail = tail.replace("_", " ").replace("-", " ").strip()
    return tail.title() or "Current"

def _guess_object_label(ctx) -> Optional[str]:
    """
    Use an object/title from the template context for detail pages if available.
    Keeps your previous convenience.
    """
    for key in ("object", "page", "post", "item", "car", "product", "entry"):
        obj = ctx.get(key)
        if not obj:
            continue
        for attr in ("title", "name"):
            if hasattr(obj, attr):
                val = getattr(obj, attr)
                return val() if callable(val) else val
        try:
            return str(obj)
        except Exception:
            pass
    return None

# -------- Friendly labels (extend as needed) --------
NAME_LABEL_MAP: Dict[str, str] = {
    # Home aliases
    "home:index": "Home",
    "index": "Home",
    "home": "Home",
    "home:about": "About",
    "home:contact": "Contact",

    # AppAttack (Projects)
    "appattack": "App Attack",
    "Appattack_Skills": "Skills",
    "appattack_join": "Join App Attack",
    "comphrehensive_reports": "Comprehensive Reports",
    "pen-testing": "Pen Testing",
    "secure-code-review": "Secure Code Review",
    "pen_testing_form": "Pen Testing Form",
    "secure_code_review_form": "Secure Code Review Form",

    # PT-GUI Viz
    "ptgui_viz_main": "PT-GUI",
    "ptgui_skills": "PT-GUI Skills",
    "ptgui_contact-us": "Contact",
    "ptgui_tools_home": "Tools",
    "tool_aircrack": "Aircrack",
    "tool_arjun": "Arjun",
    "tool_rainbowcrack": "RainbowCrack",
    "tool_airbase": "Airbase",
    "tool_amap": "AMap",
    "tool_amass": "Amass",
    "tool_arpaname": "Arpaname",
    "ptgui_join_us": "Join PT-GUI",

    # Malware Viz
    "malware_viz_main": "Malware Viz",
    "malware_skills": "Malware Skills",
    "malware_viz_joinus": "Join Malware Viz",
    "malware_products": "Products & Services",

    # Smishing Detection
    "smishing_detection_main": "Smishing Detection",
    "smishing_skills": "Smishing Skills",
    "smishingdetection_join_us": "Join Smishing",

    # Threat Mirror
    "Deakin_Threat_mirror_main": "Threat Mirror",
    "deakinthreatmirror_skills": "Threat Mirror Skills",
    "threat_mirror_join_us": "Join Threat Mirror",

    # VR
    "Vr_main": "CyberSafe VR",
    "cybersafe_vr_skills": "VR Skills",
    "cybersafe_vr_join_us": "Join VR",

    # Upskilling
    "upskilling": "Upskilling",
    "upskilling_skill": "Skill",
    "complete_skill": "Complete Skill",
    "update_progress": "Update Progress",
    "join_us": "Join Project",
    "success": "Success",
    "pages/upskilling/repository.html": "Upskilling Repository",
    "pages/upskilling/roadmap.html": "Upskilling Roadmap",
    "pages/upskilling/progress.html": "Upskilling Progress",

    # Careers
    "career-list": "Careers",
    "career-detail": "Job",
    "career-application": "Apply",
    "internships": "Internships",
    "job-alerts": "Job Alerts",
    "career-discover": "Discover Careers",

    # Blog
    "blog": "Blog",
    "detail_article": "Article",
    "like_article": "Like Article",

    # Auth / Profile
    "client_sign_in": "Client Sign In",
    "profile": "Profile",
    "profile_details": "Profile Details",
    "signup": "Sign Up",
    "login": "Login",
    "login_with_otp": "Login with OTP",
    "verify_otp": "Verify OTP",
    "verifyEmail": "Verify Email",
    "post_otp_login_captcha": "OTP Captcha",
    "passkey_login": "Passkey Login",
    "password_reset": "Password Reset",
    "password_reset_confirm": "Reset Password Confirm",
    "reset_passkeys_request": "Reset Passkeys",
    "reset_passkeys_verify": "Verify Passkeys",
    "delete-account": "Delete Account",

    # Stats / Dashboard / Misc
    "dashboard": "Dashboard",
    "project-stats": "Project Stats",
    "chart-filter-options": "Chart Filters",
    "maintenance": "Maintenance",
    "policy_deployment": "Policy Deployment",
    "reports": "Reports",
    "report_blog": "Report Blog",
    "publishedblog": "Published Blogs",
    "blogpage": "Blog Page",
    "edit_blogpage": "Edit Blog",
    "adminblogpage": "Admin Blogs",
    "approve_blogpage": "Approve Blog",
    "reject_blogpage": "Reject Blog",
    "delete_blogpage": "Delete Blog",
    "reported_blogs": "Reported Blogs",
    "download_reported_blogs": "Download Reports",
    "feedback": "Feedback",
    "delete_feedback": "Delete Feedback",
    "SearchSuggestions": "Search Suggestions",
    "pages/search-results": "Search Results",
    "pages/website-form": "Website Form",

    # Challenges / Leaderboard
    "challenge_list": "Challenges",
    "cyber_quiz": "Cyber Quiz",
    "category_challenges": "Category",
    "challenge_detail": "Challenge Detail",
    "submit_answer": "Submit Answer",
    "leaderboard": "Leaderboard",

    # APIs / Swagger
    "api-models": "API Models",
    "api-analytics": "API Analytics",
    "user-management": "User Management",
}

# -------- Parent chains (this creates the full trail) --------
PARENT_MAP: Dict[str, List[str]] = {
    # App Attack subtree
    "appattack": ["index"],
    "Appattack_Skills": ["index", "appattack"],
    "appattack_join": ["index", "appattack"],
    "comphrehensive_reports": ["index", "appattack"],
    "pen-testing": ["index", "appattack"],
    "secure-code-review": ["index", "appattack"],
    "pen_testing_form": ["index", "appattack", "pen-testing"],
    "secure_code_review_form": ["index", "appattack", "secure-code-review"],

    # PT-GUI tools nest under PT-GUI
    "ptgui_viz_main": ["index"],
    "ptgui_skills": ["index", "ptgui_viz_main"],
    "ptgui_contact-us": ["index", "ptgui_viz_main"],
    "ptgui_tools_home": ["index", "ptgui_viz_main"],
    "tool_aircrack": ["index", "ptgui_viz_main", "ptgui_tools_home"],
    "tool_arjun": ["index", "ptgui_viz_main", "ptgui_tools_home"],
    "tool_rainbowcrack": ["index", "ptgui_viz_main", "ptgui_tools_home"],
    "tool_airbase": ["index", "ptgui_viz_main", "ptgui_tools_home"],
    "tool_amap": ["index", "ptgui_viz_main", "ptgui_tools_home"],
    "tool_amass": ["index", "ptgui_viz_main", "ptgui_tools_home"],
    "tool_arpaname": ["index", "ptgui_viz_main", "ptgui_tools_home"],
    "ptgui_join_us": ["index", "ptgui_viz_main"],

    # Malware Viz
    "malware_viz_main": ["index"],
    "malware_skills": ["index", "malware_viz_main"],
    "malware_viz_joinus": ["index", "malware_viz_main"],
    "malware_products": ["index", "malware_viz_main"],

    # Smishing
    "smishing_detection_main": ["index"],
    "smishing_skills": ["index", "smishing_detection_main"],
    "smishingdetection_join_us": ["index", "smishing_detection_main"],

    # Threat Mirror
    "Deakin_Threat_mirror_main": ["index"],
    "deakinthreatmirror_skills": ["index", "Deakin_Threat_mirror_main"],
    "threat_mirror_join_us": ["index", "Deakin_Threat_mirror_main"],

    # VR
    "Vr_main": ["index"],
    "cybersafe_vr_skills": ["index", "Vr_main"],
    "cybersafe_vr_join_us": ["index", "Vr_main"],

    # Upskilling
    "upskilling": ["index"],
    "upskilling_skill": ["index", "upskilling"],
    "complete_skill": ["index", "upskilling"],
    "join_us": ["index"],
    "success": ["index", "upskilling"],
    "update_progress": ["index", "upskilling"],
    "pages/upskilling/repository.html": ["index", "upskilling"],
    "pages/upskilling/roadmap.html": ["index", "upskilling"],
    "pages/upskilling/progress.html": ["index", "upskilling"],

    # Careers
    "career-list": ["index"],
    "career-detail": ["index", "career-list"],
    "career-application": ["index", "career-list"],
    "internships": ["index", "career-list"],
    "job-alerts": ["index", "career-list"],
    "career-discover": ["index", "career-list"],

    # Blog
    "blog": ["index"],
    "detail_article": ["index", "blog"],
    "like_article": ["index", "blog"],

    # Auth / Profile
    "client_sign_in": ["index"],
    "profile": ["index"],
    "profile_details": ["index", "profile"],
    "signup": ["index"],
    "login": ["index"],
    "login_with_otp": ["index"],
    "verify_otp": ["index", "login_with_otp"],
    "verifyEmail": ["index", "login_with_otp"],
    "post_otp_login_captcha": ["index", "login_with_otp"],
    "passkey_login": ["index"],
    "password_reset": ["index"],
    "password_reset_confirm": ["index", "password_reset"],
    "reset_passkeys_request": ["index"],
    "reset_passkeys_verify": ["index", "reset_passkeys_request"],
    "delete-account": ["index", "profile"],

    # Stats / Dashboard / Misc
    "dashboard": ["index"],
    "project-stats": ["index", "dashboard"],
    "chart-filter-options": ["index", "dashboard"],
    "maintenance": ["index"],
    "policy_deployment": ["index"],

    # Blog mgmt
    "blogpage": ["index", "blog"],
    "edit_blogpage": ["index", "blog"],
    "adminblogpage": ["index", "blog"],
    "approve_blogpage": ["index", "adminblogpage"],
    "reject_blogpage": ["index", "adminblogpage"],
    "delete_blogpage": ["index", "adminblogpage"],
    "publishedblog": ["index", "blog"],
    "report_blog": ["index", "blog"],
    "reports": ["index", "blog"],
    "download_reported_blogs": ["index", "reports"],

    # Feedback
    "feedback": ["index"],
    "delete_feedback": ["index", "feedback"],

    # Search
    "SearchSuggestions": ["index"],
    "pages/search-results": ["index"],
    "pages/website-form": ["index"],
}

def _extend(crumbs: List[Crumb], names: List[str]) -> None:
    seen = {(c.label, c.url) for c in crumbs}
    for n in names:
        url = _safe_reverse(n) or "#"
        label = NAME_LABEL_MAP.get(n) or _pretty_from_view(n)
        tpl = (label, url)
        if tpl not in seen:
            crumbs.append(Crumb(label, url))
            seen.add(tpl)

@register.inclusion_tag("includes/breadcrumbs.html", takes_context=True)
def breadcrumbs(context):
    """
    Renders 'includes/breadcrumbs.html' with a 'breadcrumbs' list.
    Keeps your old behavior (Home detection, object label), adds parent-chain support.
    """
    request = context.get("request")

    # Compute a Home link (reverse if possible)
    home_url = _safe_reverse("home:index") or _safe_reverse("index") or "/"
    items: List[Crumb] = [Crumb("Home", home_url)]

    rm = getattr(request, "resolver_match", None)
    if not rm:
        return {"breadcrumbs": items}

    view_name = rm.view_name or ""
    path = getattr(request, "path", "/") or "/"

    # If homepage, show only Home (active)
    if path == "/" or view_name in {"home:index", "index", "home"}:
        return {"breadcrumbs": [Crumb("Home", None)]}

    # Add parent chain, if any
    parents = PARENT_MAP.get(view_name, [])
    _extend(items, parents)

    # Final/current label: prefer context object (detail pages), fallback to friendly map or pretty name
    obj_label = _guess_object_label(context)
    current = obj_label or NAME_LABEL_MAP.get(view_name) or _pretty_from_view(view_name)
    items.append(Crumb(current, None))

    # Compact long trails
    if len(items) > 7:
        items = items[:3] + [Crumb("…", None)] + items[-3:]

    # De-dupe adjacent labels
    deduped: List[Crumb] = []
    for c in items:
        if not deduped or deduped[-1].label != c.label:
            deduped.append(c)

    return {"breadcrumbs": deduped}

