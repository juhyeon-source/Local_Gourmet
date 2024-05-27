from django.urls import path
from rest_framework_simplejwt.views import TokenVerifyView

from .views import SignupView,LoginView

app_name = "accounts"
urlpatterns: list = [
    path("signup/", SignupView.as_view()),
    path("login/", LoginView.as_view(), name="Login_View"),
    path("api/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
]
