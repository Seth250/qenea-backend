from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth import password_validation as validators
from django.core import exceptions
import collections


UserModel = get_user_model()

class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True, required=True, style={'input_type': 'password', 'placeholder': 'Password'}
    )
    password2 = serializers.CharField(
        write_only=True, required=True, style={'input_type': 'password', 'placeholder': 'Confirm Password'}
    )

    class Meta:
        model = UserModel
        fields = ('id', 'email', 'username', 'first_name', 'last_name', 'password', 'password2')
        read_only_fields = ('id', )

    def validate(self, data):
        password = data['password']
        # since we only need one password field for User creation, we can remove the second password field
        password2 = data.pop('password2')
        errors = collections.defaultdict(list)

        if password != password2:
            errors['password2'].append('The Two password fields do not match')

        try:
            validators.validate_password(password=password2, user=UserModel)

        except exceptions.ValidationError as err:
            errors['password2'].extend(err.messages)

        if errors:
            raise serializers.ValidationError(errors)

        return super(UserSerializer, self).validate(data)

    def create(self, validated_data):
        user = UserModel.objects.create_user(**validated_data)
        return user