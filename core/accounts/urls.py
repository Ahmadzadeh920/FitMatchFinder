from django.urls import path
from django.urls import include



app_name = "accounts"

urlpatterns = [
    # path("", include("django.contrib.auth.urls")),
  
    path("api/v1/", include("accounts.api.V1.urls")),
   
]