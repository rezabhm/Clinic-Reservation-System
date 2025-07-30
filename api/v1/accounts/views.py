from apps.core.models import CustomUser
from django.utils.decorators import method_decorator
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import (
    SignupSerializer,
    LoginSerializer,
    ForgotPasswordSerializer,
    ResetPasswordSerializer,
    TokenRefreshSerializer
)
from .swagger_decorators import (
    signup_swagger,
    login_swagger,
    forgot_password_swagger,
    reset_password_swagger,
    token_refresh_swagger
)

User = CustomUser


@method_decorator(name='post', decorator=signup_swagger)
class SignupAPIView(GenericAPIView):
    """
    API view for user registration.
    """
    serializer_class = SignupSerializer

    def post(self, request, *args, **kwargs):
        """
        Handle user registration and return JWT tokens.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)


@method_decorator(name='post', decorator=login_swagger)
class LoginAPIView(GenericAPIView):
    """
    API view for user login.
    """
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        """
        Handle user login and return JWT tokens.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        user = User.objects.filter(username=username).first()
        if user and user.check_password(password):
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


@method_decorator(name='post', decorator=forgot_password_swagger)
class ForgotPasswordAPIView(GenericAPIView):
    """
    API view for handling forgot password requests.
    """
    serializer_class = ForgotPasswordSerializer

    def post(self, request, *args, **kwargs):
        """
        Handle forgot password requests.
        In a real application, this would trigger an email with a password reset link.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # In a real application, you would send an email with a reset link.
        # For this example, we'll just return a success message.
        return Response({'message': 'Password reset link sent.'}, status=status.HTTP_200_OK)


@method_decorator(name='post', decorator=reset_password_swagger)
class ResetPasswordAPIView(GenericAPIView):
    """
    API view for handling password reset requests.
    """
    serializer_class = ResetPasswordSerializer

    def post(self, request, *args, **kwargs):
        """
        Handle password reset requests.
        In a real application, this would validate the token and reset the user's password.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # In a real application, you would validate the token and reset the password.
        # For this example, we'll just return a success message.
        return Response({'message': 'Password has been reset.'}, status=status.HTTP_200_OK)


@method_decorator(name='post', decorator=token_refresh_swagger)
class TokenRefreshAPIView(GenericAPIView):
    """
    API view for refreshing JWT tokens.
    """
    serializer_class = TokenRefreshSerializer

    def post(self, request, *args, **kwargs):
        """
        Handle JWT token refresh requests.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            refresh = RefreshToken(serializer.validated_data['refresh'])
            return Response({
                'access': str(refresh.access_token),
            })
        except Exception as e:
            return Response({'error': 'Invalid refresh token'}, status=status.HTTP_400_BAD_REQUEST)
