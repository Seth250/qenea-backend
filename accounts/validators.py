import re

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from django.utils.translation import ngettext_lazy

MIN_USERNAME_LENGTH = 3
MAX_USERNAME_LENGTH = 25

regex_username_validator = RegexValidator(
    regex=r'^[a-zA-Z0-9_][a-zA-Z0-9_.]*[a-zA-Z0-9_]$',
    message=_('Username must start and end with letters, numbers or underscore but can contain period.')
)


def validate_username(value: str):
    if len(value) < MIN_USERNAME_LENGTH:
        raise ValidationError(
            _('Username must have more than %(min_length)s characters.'),
            params={'min_length': MIN_USERNAME_LENGTH}
        )

    regex_username_validator(value)
    return value


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
