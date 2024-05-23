from django.urls import path
from .views import SignupView,AccountLogInView,logout,AccountDetailView

app_name = "accounts"
urlpatterns: list = [
    path("signup/", SignupView.as_view()),
    path("login/", AccountLogInView.as_view()),
    path("logout/", logout),
    path("<str:username>/", AccountDetailView.as_view()),
]
