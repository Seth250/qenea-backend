import re
from django.core.exceptions import ValidationError
from django.utils.translation import ngettext_lazy


class NumberDigitsPasswordValidator:
    """
    Validate whether the password has the specified number of digits.
    """

    def __init__(self, min_digits=0):
        self._min_digits = min_digits

    def validate(self, password, user=None):
        if not len(re.findall('\d', password)) >= self._min_digits:
            raise ValidationError(
                message=ngettext_lazy(
                    "This password must contain at least %(min_digits)d digit, 0-9.",
                    "This password must contain at least %(min_digits)d digits, 0-9.",
                    self._min_digits
                ),
                code='password_short_digits',
                params={'min_digits': self._min_digits}
            )

    def get_help_text(self):
        return ngettext_lazy(
            "This password must contain at least %(min_digits)d digit, 0-9.",
            "This password must contain at least %(min_digits)d digits, 0-9.",
            self._min_digits
        ) % {'min_digits': self._min_digits}
