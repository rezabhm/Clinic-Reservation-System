from rest_framework import serializers
from apps.core.models import CustomUser

User = CustomUser


class SignupSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    """
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name')

    def create(self, validated_data):
        """
        Create and return a new user.
        """
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login.
    """
    username = serializers.CharField()
    password = serializers.CharField()


class ForgotPasswordSerializer(serializers.Serializer):
    """
    Serializer for the forgot password functionality.
    """
    email = serializers.EmailField()


class ResetPasswordSerializer(serializers.Serializer):
    """
    Serializer for the reset password functionality.
    """
    token = serializers.CharField()
    password = serializers.CharField()

class TokenRefreshSerializer(serializers.Serializer):
    """
    Serializer for refreshing JWT tokens.
    """
    refresh = serializers.CharField()
