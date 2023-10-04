from rest_framework import serializers

from .models import UserAccount, PreTrial, Lawyer, Judge
from django.contrib.auth import authenticate


# Serializer for base user registration
class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for base user registration.

    This serializer is used to validate base user registration data.

    Attributes:
        email (serializers.EmailField): Email field for user email.
        password (serializers.CharField): Password field for user password.
        name (serializers.CharField): Char field for user name.
        user_type (serializers.CharField): Char field for user type.

    Methods:
        validate(data): Validates the user registration data and returns the validated data.

    """

    class Meta:
        model = UserAccount
        fields = ["email", "password", "name"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    def validate(self, data):
        email = data.get("email", None)
        password = data.get("password", None)
        name = data.get("name", None)

        if email is None:
            raise serializers.ValidationError(
                'An email address is required to register for user.'
            )
        if password is None:
            raise serializers.ValidationError(
                'A password is required to register for user.'
            )
        if name is None:
            raise serializers.ValidationError(
                'A name is required to register for user.'
            )
        return data

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


class LawyerRegisterationSerializer(serializers.ModelSerializer):
    """
    Serializer for Lawyer registration.
    """
    class Meta:
        model = Lawyer
        fields = "__all__"

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    def validate(self, data):
        bar_code = data.get("bar_code", None)
        user = data.get("user", None)
        if user is None:
            raise serializers.ValidationError(
                'A user id is required to register for lawyer.'
            )
        if bar_code is None:
            raise serializers.ValidationError(
                'A bar code is required to register for lawyer.'
            )

        return data


class JudgeRegisterationSerializer(serializers.ModelSerializer):
    """
    Serializer for Lawyer registration.
    """
    class Meta:
        model = Judge
        fields = "__all__"

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    def validate(self, data):
        bar_code = data.get("bar_code", None)
        user = data.get("user", None)
        if user is None:
            raise serializers.ValidationError(
                'A user id is required to register for judge.'
            )
        if bar_code is None:
            raise serializers.ValidationError(
                'A bar code is required to register for judge.'
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
