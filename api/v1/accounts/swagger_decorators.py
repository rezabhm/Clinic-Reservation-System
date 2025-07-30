from drf_yasg.utils import swagger_auto_schema
from .serializers import (
    SignupSerializer,
    LoginSerializer,
    ForgotPasswordSerializer,
    ResetPasswordSerializer,
    TokenRefreshSerializer
)

signup_swagger = swagger_auto_schema(
    operation_summary='User Signup',
    operation_description='Creates a new user account.',
    request_body=SignupSerializer,
    responses={
        201: 'User created successfully.',
        400: 'Invalid input.'
    }
)

login_swagger = swagger_auto_schema(
    operation_summary='User Login',
    operation_description='Authenticates a user and returns a JWT token.',
    request_body=LoginSerializer,
    responses={
        200: 'Login successful.',
        401: 'Invalid credentials.'
    }
)

forgot_password_swagger = swagger_auto_schema(
    operation_summary='Forgot Password',
    operation_description='Sends a password reset link to the user\'s email.',
    request_body=ForgotPasswordSerializer,
    responses={
        200: 'Password reset link sent.'
    }
)

reset_password_swagger = swagger_auto_schema(
    operation_summary='Reset Password',
    operation_description='Resets the user\'s password using a token.',
    request_body=ResetPasswordSerializer,
    responses={
        200: 'Password has been reset.'
    }
)

token_refresh_swagger = swagger_auto_schema(
    operation_summary='Refresh Token',
    operation_description='Refreshes an expired JWT access token.',
    request_body=TokenRefreshSerializer,
    responses={
        200: 'Token refreshed successfully.',
        400: 'Invalid refresh token.'
    }
)
