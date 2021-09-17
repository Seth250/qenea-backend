from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth import get_user_model
from django.core import exceptions as django_exceptions
from django.core.validators import RegexValidator
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _
from profiles.models import Profile
import collections


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


class UserCreateSerializer(serializers.ModelSerializer):
    username = SerializerUsernameField(write_only=True)
    password = serializers.CharField(style={'input_type': 'password', 'placeholder': 'Password'}, write_only=True)
    password2 = serializers.CharField(style={'input_type': 'password', 'placeholder': 'Confirm Password'}, write_only=True)

    default_error_messages = {
        'cannot_create': _('Unable to create account.'),
        'password_mismatch': _('The two password fields didn\'t match.')
    }

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'username', 'password', 'password2')

    def validate(self, attrs):
        password = attrs.get('password')
        # since only one password field is needed for user creation, we can remove the second password field
        password2 = attrs.pop('password2')

        errors = collections.defaultdict(list)
        if password != password2:
            errors['password2'].append(self.error_messages['password_mismatch'])

        try:
            validate_password(password=password, user=User)
        except django_exceptions.ValidationError as err:
            errors['password2'].extend(err.messages)

        if errors:
            raise serializers.ValidationError(errors)

        return attrs

    def create(self, validated_data):
        username = validated_data.pop('username')

        try:
            user = User.objects.create_user(**validated_data)
        except:
            self.fail('cannot_create')

        Profile.objects.create(user=user, username=username)
        return user
