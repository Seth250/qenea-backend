import logging

from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core import exceptions as django_exceptions
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.validators import UniqueValidator

from accounts.messages import Messages
from accounts.validators import (MAX_USERNAME_LENGTH, MIN_USERNAME_LENGTH,
                                 regex_username_validator)

logger = logging.getLogger(__name__)

User = get_user_model()


class SerializerUsernameField(serializers.CharField):
    """
    Custom serializer field for case insensitive username validation
    """
    default_error_messages = {
        'non_unique': Messages.NON_UNIQUE_USERNAME
    }

    def __init__(self, **kwargs):
        kwargs['min_length'] = MIN_USERNAME_LENGTH
        kwargs['max_length'] = MAX_USERNAME_LENGTH
        super().__init__(**kwargs)

    def run_validation(self, data=...):
        qs = User.objects.all()
        try:
            # retrieving the request object here since it's not present in __init__
            request = self.context['request']
            # if it is an update method, the username of the current user is excluded from the unique validation
            # this is done so as to prevent unique constraint errors when the username isn't changed (or when
            # only the casing is changed)
            if request.method == 'PUT' or request.method == 'PATCH':
                qs = qs.exclude(pk=request.user.id)
        except:
            pass

        unique_validator = UniqueValidator(queryset=qs, message=self.error_messages['non_unique'], lookup='iexact')
        self.validators.extend([unique_validator, regex_username_validator])
        return super().run_validation(data=data)


class UserCreateSerializer(serializers.ModelSerializer):
    username = SerializerUsernameField() # overriding the default with our custom field
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    default_error_messages = {
        'cannot_create_user': _('Unable to create account.')
    }

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password')

    def validate_password(self, password):
        try:
            validate_password(password=password, user=User)
        except django_exceptions.ValidationError as e:
            # since the error is raised in a field validation, the serializer field is automatically added as the key for
            # the error (field does not need to be explicitly added since it's not an object/non field validation)
            raise serializers.ValidationError(e.messages)

        return password

    def create(self, validated_data):
        try:
            user = User.objects.create_user(**validated_data)
            # NOTE: the profile is created in the manager
        except Exception as e:
            logger.error(e)
            self.fail('cannot_create_user')
            
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
    auth_token = serializers.CharField(
        label=_('Auth Token'),
        read_only=True
    )
    username = serializers.CharField(
        label=_('Username'),
        read_only=True
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
    username = SerializerUsernameField()

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username')
        read_only_fields = ('email', )


class ObjectUserSerializer(serializers.Serializer):
    username = serializers.CharField(read_only=True)
    profile_picture = serializers.ImageField(source='profile.picture')


class EmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    message = serializers.CharField(
        read_only=True,
        default='If an account exists, you would receive an email with further instructions.'
    )

    def validate(self, attrs):
        email = attrs.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = ''

        attrs['user'] = user
        return attrs


class SetNewPasswordSerializer(serializers.Serializer):
    uidb64 = serializers.CharField(write_only=True)
    token = serializers.CharField(write_only=True)
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    message = serializers.CharField(read_only=True, default='Password has been reset successfully!')

    def validate(self, attrs):
        uidb64 = attrs.get('uidb64')
        token = attrs.get('token')
        id_ = force_str(urlsafe_base64_decode(uidb64))

        try:
            user = User.objects.get(id=id_)
        except User.DoesNotExist:
            raise NotFound('Could not find a matching account.')

        if not PasswordResetTokenGenerator().check_token(user, token):
            raise PermissionDenied(Messages.INVALID_TOKEN)

        attrs['user'] = user
        return attrs

    def validate_password(self, password):
        try:
            validate_password(password=password, user=User)
        except django_exceptions.ValidationError as e:
            raise serializers.ValidationError(e.messages)

        return password

    def save(self):
        user = self.validated_data['user']
        password = self.validated_data['password']
        user.set_password(password)
        user.save()
        