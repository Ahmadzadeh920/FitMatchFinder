from django.urls import path
from django.urls import include



app_name = "FashionClip"

urlpatterns = [
    # path("", include("django.contrib.auth.urls")),
  
    path("api/v1/", include("fashin_clip_recommendations.api.v1.urls")),
   
]