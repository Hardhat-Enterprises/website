import re

from django.core import validators
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _

@deconstructible
class StudentIdValidator(validators.RegexValidator):
    regex = r"^\d{9}$"
    message = _(
        "Enter a valid student ID. This value must contain 9 digits only"
    )
    flags = 0