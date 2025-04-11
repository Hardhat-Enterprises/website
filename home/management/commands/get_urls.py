from django.core.management.base import BaseCommand
from django.urls import URLPattern, URLResolver, get_resolver


def list_urls(urlpatterns, prefix=''):
    urls = []
    for pattern in urlpatterns:
        if isinstance(pattern, URLPattern):
            full_url = prefix + str(pattern.pattern)
            full_url = full_url.lstrip("/")
            if not full_url.startswith("admin/"):
                urls.append("http://localhost:8000/" + full_url)
        elif isinstance(pattern, URLResolver):
            nested_prefix = prefix + str(pattern.pattern)
            urls += list_urls(pattern.url_patterns, nested_prefix)
    return urls


class Command(BaseCommand):
    help = 'Export all urls to log file'

    def handle(self, *args, **options):
        resolver = get_resolver()
        urls = list_urls(resolver.url_patterns)
        with open("home/tests/logs/url_list.txt", "w", encoding="utf-8") as f:
            for url in urls:
                f.write(url + "\n")
        self.stdout.write(self.style.SUCCESS(f"✅ Export {len(urls)} URLs to url_list.txt"))
