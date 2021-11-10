from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

MIN_TAG_LENGTH = 2
MAX_TAG_LENGTH = 35


regex_tag_validator = RegexValidator(
    regex=r'^[a-z0-9][a-z0-9-]*[a-z0-9]$',
    message=_('Tag must start and end with lowercase letters or numbers, but can contain hyphens')
)


def validate_tag(value: str):
    if len(value) < MIN_TAG_LENGTH:
        raise ValidationError(
            _('Tag must have at least %(min_length)s characters.'),
            params={'min_length': MIN_TAG_LENGTH}
        )
    elif len(value) > MAX_TAG_LENGTH:
        raise ValidationError(
            _('Tag must not have more than %(max_length)s characters.'),
            params={'max_length': MAX_TAG_LENGTH}
        )
        
    regex_tag_validator(value)
    return value
