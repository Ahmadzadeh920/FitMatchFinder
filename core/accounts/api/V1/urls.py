from django.urls import path
from django.urls import include
from rest_framework.authtoken.views import ObtainAuthToken

# simple JWT
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
    TokenBlacklistView
)

from .views import *

app_name = "api_v1"
urlpatterns = [
    # registeration_process 
    path('register/',RegisterationApiview.as_view(), name='register'),
    path("activate/jwt/<str:token>", ActivationAccountJWT.as_view(), name="activation_account_jwt",),
    path('resend-validation/', ResendValidationEmailView.as_view(), name='resend-validation-email'),

    # login and Logout
    path('login_customized/', CustimizedTokenObtainPairView.as_view(), name= 'login_jwt'),
    path('logout-jwt/', TokenBlacklistView.as_view(), name='token_blacklist'),
   

   # reset password
    path('customized-request-reset-pass/',RequestPasswordReset.as_view(), name='customized-request-reset-pass'),
    path("reset/pass/<str:token>/", ResetPassword.as_view(),name="Token_reset_password",),
    path("change_password/", ChangePasswordView.as_view(), name="auth_change_password"),

    # Profile
    path( "profile/", ProfileApiView.as_view(), name="profile_api_view",),
    
]