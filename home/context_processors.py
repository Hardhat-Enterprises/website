# # home/context_processors.py
# from django.utils.text import capfirst
# from django.conf import settings

# def dynamic_page_title(request):
#     # Extract the path and capitalize it
#     path = request.path.strip("/").replace("-", " ").replace("_", " ")
#     if not path or path == "index":
#         page_title = "Home"
#     else:
#         page_title = capfirst(path)

#     # Add your site name to the title
#     full_title = f"{page_title} - Hardhat Enterprises"
#     return {"dynamic_title": full_title}

# # def dynamic_page_title(request):
# #     custom_titles = {
# #         "/about-us/": "About Us",
# #         "/contact/": "Contact Us",
# #         "/projects/": "Our Projects",
# #     }
# #     path = request.path
# #     page_title = custom_titles.get(path, capfirst(path.strip("/").replace("-", " ").replace("_", " ")))
# #     if not page_title or page_title == "Index":
# #         page_title = "Home"

# #     full_title = f"{page_title} - Hardhat Enterprises"
# #     return {"dynamic_title": full_title}

# def recaptcha_site_key(request):
#     return {
#         'RECAPTCHA_SITE_KEY': settings.RECAPTCHA_SITE_KEY
#     }



# home/context_processors.py
from django.utils.text import capfirst
from django.utils.translation import gettext as _
from django.conf import settings

from .models import UserScore
import re

def _prettify_from_path(path: str) -> str:
    
    slug = path.strip("/").replace("-", " ").replace("_", " ")
    slug = re.sub(r"\s+", " ", slug).strip()
    return capfirst(slug) if slug else "Home"


def dynamic_page_title(request):

    # Standardized path: Ensure that it ends with a slash to facilitate dictionary matching.
    path = request.path
    if not path.endswith("/"):
        path = path + "/"

    # Authoritative title of known routes 
    known_titles = {
        "/":               _("Home"),
        "/index/":         _("Home"),
        "/about-us/":      _("About Us"),
        "/about/":         _("About Us"),
        "/what-we-do/":    _("What we do"),
        "/contact/":       _("Contact Us"),
        "/projects/":      _("Our Projects"),
        "/upload/":        _("Upload Image"),
        "/blogpage/":      _("Blog"), 
        "/publishedblog/": _("Published Blogs"), 
        "/careers/discover/": _("Discover Hardhat"),
        "/careers/internships/": _("Internships"),
        "/careers/job-alerts/": _("Job Alerts"),
        "/challenges/": _("Cyber Challenges"),
        "/challenges/quiz/": _("Quiz"),
    }

    if path in known_titles:
        page_title = known_titles[path]
    else:
        # automatically generated based on the path, then sent to _() for .po translation.
        auto_title = _prettify_from_path(path)
        page_title = _(auto_title)

    
    full_title = f"{page_title} - Hardhat Enterprises"
    return {"dynamic_title": full_title}

def recaptcha_site_key(request):

    return {
        'RECAPTCHA_SITE_KEY': settings.RECAPTCHA_SITE_KEY
    }

def user_scores(request):
    """Add user scores to context for navigation display"""
    if request.user.is_authenticated:
        user_scores = UserScore.objects.filter(user=request.user).order_by('-score')
        total_score = sum(score.score for score in user_scores)
        return {
            'user_scores': user_scores,
            'user_total_score': total_score
        }
    return {}

    return {'RECAPTCHA_SITE_KEY': settings.RECAPTCHA_SITE_KEY}

