from django.urls import path
from django.urls import include
from rest_framework.authtoken.views import ObtainAuthToken

# simple JWT
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

app_name = "api_v1"
urlpatterns = [

    
]