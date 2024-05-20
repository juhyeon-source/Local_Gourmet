from django.urls import path
from .views import *

app_name = "accounts"
urlpatterns: list = [
    path("signup/", signup),
    path("login/", AccountLogInView.as_view()),
    path("logout/", logout),
    path("<str:username>/", AccountDetailView.as_view()),
]
