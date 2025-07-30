from django.urls import path
from api.v1.accounts.views import (
    SignupAPIView,
    LoginAPIView,
    ForgotPasswordAPIView,
    ResetPasswordAPIView,
    TokenRefreshAPIView,
)

app_name = 'accounts'

urlpatterns = [
    path('signup/', SignupAPIView.as_view(), name='signup'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('forgot-password/', ForgotPasswordAPIView.as_view(), name='forgot-password'),
    path('reset-password/', ResetPasswordAPIView.as_view(), name='reset-password'),
    path('token/refresh/', TokenRefreshAPIView.as_view(), name='token-refresh'),
]
