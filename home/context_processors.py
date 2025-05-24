# home/context_processors.py
from django.utils.text import capfirst
from django.conf import settings

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