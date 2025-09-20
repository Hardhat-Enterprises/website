import nh3
import re
import unicodedata
from django.core.exceptions import ValidationError
from home.validators import xss_detection

def clean_text(value: str) -> str:
    if not value:
        return ""
    value = xss_detection(value)
    return nh3.clean(value, tags=set(), attributes={})

def clean_html(value: str) -> str:
    if not value:
        return ""
    return nh3.clean(
        value,
        tags={"b", "i", "u", "em", "strong", "a", "p", "ul", "ol", "li"},
        attributes={"a": ["href", "title"]}
    )

def clean_url(value: str) -> str:
    if not value:
        return ""
    value = value.strip()
    pattern = re.compile(r'^(https?://[^\s/$.?#].[^\s]*)$', re.IGNORECASE)
    if not pattern.match(value):
        raise ValidationError("Invalid URL format")
    return value

def clean_email(value: str) -> str:
    if not value:
        return ""
    value = value.strip().lower()
    pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    if not pattern.match(value):
        raise ValidationError("Invalid email format")
    return value

def clean_numeric(value: str) -> str:
    if not value:
        return ""
    value = value.strip()
    if not value.isdigit():
        raise ValidationError("This field accepts digits only.")
    return value

def normalize_input(value: str) -> str:
    if not value:
        return ""
    return unicodedata.normalize("NFC", value).strip()
