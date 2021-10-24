from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions as django_exceptions
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

User = get_user_model()


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type': 'password', 'placeholder': 'Password'}, write_only=True)

    default_error_messages = {
        'cannot_create_user': _('Unable to create account.')
    }

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'username', 'password')

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
        fields = ('id', 'first_name', 'last_name', 'email', 'username')
        read_only_fields = ('id', 'email')


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
