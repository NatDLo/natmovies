from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from django.contrib.auth.hashers import make_password
from .models import User
from django.utils.translation import gettext_lazy as _

class UserRegisterSerializer(ModelSerializer):
    """
    Serializer for registering a new user.
    Handles user creation with password hashing and email validation.
    """

    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True, min_length=6)

    class Meta:  # Meta information for the serializer
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 'password'
        ]
        extra_kwargs = {
            "is_active": {"read_only": True},  # Read-only
            "date_joined": {"read_only": True}  # Read-only
        }

    def validate_email(self, value):
        """
        Validates that the email is not already registered
        arguments:
        value -- email to validate
        returns: email if valid
        """
        user_id = self.instance.id if self.instance else None
        if User.objects.filter(email=value).exclude(id=user_id).exists():
            raise serializers.ValidationError(_("Este email ya está registrado."))
        return value

    def create(self, validated_data):
        """
        Creates a new user with the hashed password

        arguments:
        validated_data -- validated data from the serializer
        returns: instance of the created user
        """
        # Extract fields that should NOT go to create_user
        validated_data.pop('groups', None)
        validated_data.pop('user_permissions', None)
        
        password = validated_data.pop('password')
        user = User.objects.create_user(password=password, **validated_data)
        return user