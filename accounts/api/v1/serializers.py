from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core import exceptions as django_exceptions
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from rest_framework.exceptions import NotFound, PermissionDenied

User = get_user_model()


class UserCreateSerializer(serializers.ModelSerializer):
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
        except:
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
        fields = ('first_name', 'last_name', 'email', 'username')
        read_only_fields = ('email', )


class ObjectUserSerializer(serializers.Serializer):
    username = serializers.ReadOnlyField()
    profile_picture = serializers.ImageField(source='profile.picture')


class EmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)

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

    def validate(self, attrs):
        uidb64 = attrs.get('uidb64')
        token = attrs.get('token')
        id_ = force_str(urlsafe_base64_decode(uidb64))

        try:
            user = User.objects.get(id=id_)
        except User.DoesNotExist:
            raise NotFound('No such account exists.')

        if not PasswordResetTokenGenerator().check_token(user, token):
            raise PermissionDenied('Token is not valid, please request a new one.')

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
        