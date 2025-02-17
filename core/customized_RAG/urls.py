from django.urls import path
from django.urls import include



app_name = "CustomizedRAG"

urlpatterns = [
    # path("", include("django.contrib.auth.urls")),
  
    path("api/v1/", include("customized_RAG.api.v1.urls")),
   
]