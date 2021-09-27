import collections

from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions as django_exceptions
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from rest_framework.exceptions import NotFound
from rest_framework.validators import UniqueValidator

from accounts.validators import MAX_USERNAME_LENGTH, MIN_USERNAME_LENGTH, regex_username_validator


User = get_user_model()

class SerializerUsernameField(serializers.CharField):
    default_error_messages = {
        'non_unique': _('This username already exists.')
    }

    def __init__(self, **kwargs):
        kwargs['min_length'] = MIN_USERNAME_LENGTH
        kwargs['max_length'] = MAX_USERNAME_LENGTH
        super().__init__(**kwargs)
        unique_validator = UniqueValidator(queryset=User.objects.all(), message=self.error_messages['non_unique'], lookup='iexact')
        self.validators.extend([unique_validator, regex_username_validator])


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
        try:
            user = User.objects.create_user(**validated_data)
            # NOTE: the profile is created in the manager
        except:
            self.fail('cannot_create')
            
        return user


class AuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField(
        label=_('Email Address'),
        write_only=True
    )
    password = serializers.CharField(
        label=_('Password'),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )

    default_error_messages = {
        'invalid_credentials': _('Email and password combination is not correct.'),
        'incomplete_credentials': _('Must include "email" and "password".')
    }

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'), email=email, password=password)
            if not user:
                self.fail('invalid_credentials')

        else:
            self.fail('incomplete_credentials')

        attrs['user'] = user
        return attrs


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'username')
        read_only_fields = ('id', 'email')


class EmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)

    default_error_messages = {
        'not_found': _('User with the given email does not exist.')
    }

    def validate(self, attrs):
        email = attrs.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise NotFound(self.error_messages['not_found'])

        attrs['user'] = user
        return attrs