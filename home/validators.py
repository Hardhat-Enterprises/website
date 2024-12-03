import re

from django.core import validators
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

#For Validation
def xss_detection(input_data):
        pattern = r"<\\s*script\\b[^>]*>[^<]+<\\s*\\/\\s*script\\s*>"
        if re.search(pattern, input_data, re.IGNORECASE):
            raise ValidationError(f"XSS Attack Detected: {input_data}")
        return input_data

@deconstructible
class StudentIdValidator(validators.RegexValidator):
    regex = r"^\d{9}$"
    message = _(
        "Enter a valid student ID. This value must contain 9 digits only"
    )
    flags = 0