from rest_framework import serializers

from .models import UserAccount, PreTrial
from django.contrib.auth import authenticate


# Serializer for user registration
class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ["email", "name", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

# Serializer for user login


class UserLoginSerializer(serializers.ModelSerializer):
    """
    Serializer for user login.

    This serializer is used to validate user login credentials and authenticate the user.

    Attributes:
        email (serializers.EmailField): Email field for user email.
        password (str): Password field for user password.

    Methods:
        validate(data): Validates the user login credentials and returns the validated data.

    """
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = UserAccount
        fields = ["email", "password"]

    def validate(self, data):
        email = data.get("email", None)
        password = data.get("password", None)
        if email is None:
            raise serializers.ValidationError(
                'An email address is required to log in.'
            )
        user = authenticate(email=email, password=password)
        if user is None:
            raise serializers.ValidationError(
                'A user with this email is not found.'
            )
        return data

# Serializer for Entry model


class PreTrialSerializer(serializers.ModelSerializer):
    """
    A serializer for the PreTrial model.

    This serializer serializes all fields of the PreTrial model.
    """
    class Meta:
        model = PreTrial
        fields = "__all__"
