from django.urls import path
from django.urls import include
from rest_framework.authtoken.views import ObtainAuthToken

# simple JWT
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from .views import RegisterationApiview, ActivationAccountJWT 

app_name = "api_v1"
urlpatterns = [
    # registeration_process 
    path('register/',RegisterationApiview.as_view(), name='register'),
    path("activate/jwt/<str:token>", ActivationAccountJWT.as_view(), name="activation_account_jwt",),
   
    
]