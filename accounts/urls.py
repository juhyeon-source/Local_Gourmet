from django.urls import path
from django.urls.conf import include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenVerifyView

from .views import (
    SignupView,
    LoginView,
    BookmarkViewSet,
    UserDeleteAPIView,
    SocialUrlView,
    KakaoLoginView,
    GoogleLoginView,
    AccountsDetailView,
)

router = DefaultRouter()
router.register(r"bookmarks", BookmarkViewSet)


app_name = "accounts"
urlpatterns: list = [
    path("", include(router.urls)),
    path("signup/", SignupView.as_view()),
    path("delete-account/", UserDeleteAPIView.as_view(), name="delete-account"),
    path("login/", LoginView.as_view(), name="Login_View"),
    path("me/", AccountsDetailView.as_view(), name="accounts-detail"),
    path("api/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("social/", SocialUrlView.as_view(), name="social_login"),
    path("kakao/", KakaoLoginView.as_view(), name="kakao_login"),
    path("google/", GoogleLoginView.as_view(), name="google_login"),
]
