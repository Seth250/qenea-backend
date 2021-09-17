from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from profiles.models import Profile


User = get_user_model()

class SerializerUsernameField(serializers.CharField):
    default_error_messages = {
        'non_unique': _('This username already exists.'),
        'invalid': _('Username can only contain letters, numbers or underscore.')
    }

    def __init__(self, max_length=25, **kwargs):
        kwargs['max_length'] = max_length
        super().__init__(**kwargs)
        unique_validator = UniqueValidator(queryset=Profile.objects.all(), message=self.error_messages['non_unique'], lookup='iexact')
        regex_validator = RegexValidator(regex=r'^[a-zA-Z0-9_]*$', message=self.error_messages['invalid'])
        self.validators.extend([unique_validator, regex_validator])
