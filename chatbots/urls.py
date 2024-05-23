from django.urls import path
from .  import views

urlpatterns = [
    path("chatbot/", views.ChatbotsAPIView.as_view(), name="chatbot"),
]
