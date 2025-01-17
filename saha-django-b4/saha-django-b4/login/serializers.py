from rest_framework import serializers
from .models import User
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8, required=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'role', 'skills', 'preferences']  # Use 'skills' for consistency.

    def validate_password(self, value):
        """
        Add password validation logic, such as minimum length or complexity requirements.
        """
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        if not any(char.isdigit() for char in value):
            raise serializers.ValidationError("Password must contain at least one number.")
        if not any(char.isupper() for char in value):
            raise serializers.ValidationError("Password must contain at least one uppercase letter.")
        if not any(char in "!@#$%^&*()_+" for char in value):
            raise serializers.ValidationError("Password must contain at least one special character.")
        return value

    def create(self, validated_data):
        """
        Hash the password and create a new user instance.
        """
        try:
            password = validated_data.pop('password')
            validated_data['password'] = make_password(password)
            user = User.objects.create(**validated_data)
            return user
        except Exception as e:
            raise ValidationError(f"An error occurred during user creation: {str(e)}")
