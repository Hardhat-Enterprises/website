# home/context_processors.py
from django.utils.text import capfirst
from django.conf import settings
from .models import UserScore

def dynamic_page_title(request):
    # Extract the path and capitalize it
    path = request.path.strip("/").replace("-", " ").replace("_", " ")
    if not path or path == "index":
        page_title = "Home"
    else:
        page_title = capfirst(path)

    # Add your site name to the title
    full_title = f"{page_title} - Hardhat Enterprises"
    return {"dynamic_title": full_title}

def dynamic_page_title(request):
    custom_titles = {
        "/about-us/": "About Us",
        "/contact/": "Contact Us",
        "/projects/": "Our Projects",
    }
    path = request.path
    page_title = custom_titles.get(path, capfirst(path.strip("/").replace("-", " ").replace("_", " ")))
    if not page_title or page_title == "Index":
        page_title = "Home"

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