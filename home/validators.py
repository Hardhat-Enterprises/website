import re

from django.core import validators
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import check_password
from django.apps import apps

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

# Password History Validator

class PasswordHistoryValidator:
    """
    Prevents reusing recent passwords.
    """
    def __init__(self, keep_last=2, include_current=True):
        self.keep_last = int(keep_last)
        self.include_current = bool(include_current)

    def validate(self, password, user=None):
        if user is None or not getattr(user, "pk", None):
            return

        # Block reusing the current password
        if self.include_current and user.password and check_password(password, user.password):
            raise ValidationError(
                _("You cannot reuse your current password."),
                code="password_no_reuse_current",
            )

        if self.keep_last <= 0:
            return

        PasswordHistory = apps.get_model("home", "PasswordHistory")
        recent = PasswordHistory.objects.filter(user=user).order_by("-created_at")[: self.keep_last]
        for entry in recent:
            if check_password(password, entry.encoded_password):
                raise ValidationError(
                    _("You cannot reuse one of your recent passwords."),
                    code="password_no_reuse_history",
                )

    def get_help_text(self):
        return _("You cannot reuse your last %(n)d passwords.") % {"n": self.keep_last}

    def password_changed(self, password, user=None):
        """
        Store the new encoded password and prune to keep_last.
        """

        # We store history via signals (pre_save)

        #if user is None or not getattr(user, "pk", None) or not user.password:
            #return

        #PasswordHistory = apps.get_model("home", "PasswordHistory")
        #PasswordHistory.objects.create(user=user, encoded_password=user.password)

        #if self.keep_last <= 0:
            #return

        #ids_to_keep = list(
            #PasswordHistory.objects.filter(user=user)
            #.order_by("-created_at")
            #.values_list("id", flat=True)[: self.keep_last]
        #)
        #PasswordHistory.objects.filter(user=user).exclude(id__in=ids_to_keep).delete()

        pass

class ComplexityPasswordValidator:

    def __init__(
        self,
        require_lower=True,
        require_upper=True,
        require_digit=True,
        require_symbol=True,
        symbols=r"[@$!%*?&]"
    ):
        self.require_lower = require_lower
        self.require_upper = require_upper
        self.require_digit = require_digit
        self.require_symbol = require_symbol
        self.symbols = symbols

    def validate(self, password, user=None):
        errors = []

        if self.require_lower and not re.search(r"[a-z]", password):
            errors.append(_("Password must include at least one lowercase letter."))

        if self.require_upper and not re.search(r"[A-Z]", password):
            errors.append(_("Password must include at least one uppercase letter."))

        if self.require_digit and not re.search(r"\d", password):
            errors.append(_("Password must include at least one number."))

        if self.require_symbol and not re.search(self.symbols, password):
            errors.append(_("Password must include at least one special character (@, $, !, %, *, ?, &)."))

        if errors:
            raise ValidationError(errors)

    def get_help_text(self):
        return _(
            "Your password must include at least one lowercase letter, one uppercase letter, one number, "
            "and one special character (@, $, !, %, *, ?, &)."
        )