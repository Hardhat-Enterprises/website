from django.test import TestCase

# Create your tests here.

#Testing Validation
import re
from django.core.exceptions import ValidationError

def xss_detection(input_data):
    pattern = r"<\s*script\b[^>]*>.*?<\s*/\s*script\s*>"
    if re.search(pattern, input_data, re.IGNORECASE):
        print(f"XSS Attack Detected: {input_data}")
        raise ValidationError(f"XSS Attack Detected: {input_data}")
    return input_data

# Test for Contact in terms of Validation
xss_detection("<script>alert('XSS')</script>")
xss_detection("hello")