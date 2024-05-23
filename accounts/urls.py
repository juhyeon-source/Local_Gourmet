from django.urls import path
from rest_framework_simplejwt.views import TokenVerifyView

from .views import SignupView, AccountLogInView, logout, AccountDetailView

app_name = "accounts"
urlpatterns: list = [
    path("signup/", SignupView.as_view()),
    path("login/", AccountLogInView.as_view()),
    path("logout/", logout),
    path("<str:username>/", AccountDetailView.as_view()),
    path("api/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
]
