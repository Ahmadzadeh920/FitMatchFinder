from django.urls import path
from django.urls import include



app_name = "AIChatBot"

urlpatterns = [
    # path("", include("django.contrib.auth.urls")),
  
    path("api/v1/", include("AI_chat_bot.api.v1.urls")),
   
]