import secrets

import requests
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password

from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    DestroyAPIView,
    RetrieveUpdateAPIView,
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import viewsets, status

from local_gourmet import settings
from reviews.models import Review, Comment

# from allauth.socialaccount.providers.kakao import views as kakao_view

from .models import Bookmark
from .serializers import (
    SignupSerializer,
    LoginSerializer,
    ProfileSerializer,
    BookmarkSerializer,
    UserSerializer,
    AccountsSerializer,
    ReviewSerializer,
    CommentSerializer,
)

User = get_user_model()


class SignupView(CreateAPIView):
    """
    signup: 회원 가입 FBV
    """

    model = get_user_model()
    serializer_class = SignupSerializer
    permission_classes = [AllowAny]  # 회원가입은 누구나 할 수 있기 때문에 AllowAny 사용


class UserDeleteAPIView(DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        password = request.data.get("password")

        if not check_password(password, user.password):
            return Response(
                {"error": "비밀번호가 올바르지 않습니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.delete()
        return Response(
            {"message": "계정이 성공적으로 삭제되었습니다."},
            status=status.HTTP_204_NO_CONTENT,
        )


class Profile(ListAPIView):
    model = get_user_model()
    serializer_class = ProfileSerializer
    # FIXME: permission 나중에 수정 예정
    permission_classes = [AllowAny]


class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer


class BookmarkViewSet(viewsets.ModelViewSet):
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # 사용자 별로 북마크 조회 제한
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        # 북마크 생성 시, 자동으로 사용자 할당
        serializer.save(user=self.request.user)


class AccountsDetailView(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = AccountsSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)

        try:
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def perform_update(self, serializer):
        serializer.save()


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        user = request.user
        data = request.data

        current_password = data.get("current_password")
        new_password = data.get("new_password")
        new_password_check = data.get("new_password_check")

        if not current_password or not new_password or not new_password_check:
            return Response(
                {"error": "모든 필수 정보를 입력해주세요."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if new_password != new_password_check:
            return Response(
                {"error": "새 비밀번호가 새 비밀번호 확인과 일치하지 않습니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not check_password(current_password, user.password):
            return Response(
                {"error": "현재 비밀번호가 올바르지 않습니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if new_password == current_password:
            return Response(
                {"error": "새 비밀번호는 현재 비밀번호와 달라야 합니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.set_password(new_password)
        user.save()

        return Response(
            {"success": "비밀번호가 성공적으로 변경되었습니다."},
            status=status.HTTP_200_OK,
        )


class BookmarkListView(ListAPIView):
    serializer_class = BookmarkSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Bookmark.objects.filter(user=self.request.user)


class UserReviewListView(ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Review.objects.filter(user=self.request.user)


class UserCommentListView(ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Comment.objects.filter(user=self.request.user)


# BASE_URL = f"{settings.BASE_URL}"


BASE_URL = "http://127.0.0.1:8000"  # 예시 BASE URL
STATE = secrets.token_urlsafe(16)


class SocialUrlView(APIView):
    def post(self, request):
        social = request.data.get("social", None)
        if social is None:
            return Response(
                {"error": "소셜로그인이 아닙니다"}, status=status.HTTP_400_BAD_REQUEST
            )
        elif social == "kakao":
            url = (
                "https://kauth.kakao.com/oauth/authorize?client_id="
                + settings.KAKAO_REST_API_KEY
                + "&redirect_uri="
                + BASE_URL
                + "&response_type=code&prompt=login"
            )
            return Response({"url": url}, status=status.HTTP_200_OK)
        elif social == "google":
            client_id = settings.SOCIAL_AUTH_GOOGLE_CLIENT_ID
            redirect_uri = BASE_URL
            url = f"https://accounts.google.com/o/oauth2/v2/auth?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code&scope=email%20profile"
            return Response({"url": url}, status=status.HTTP_200_OK)


class KakaoLoginView(APIView):
    def post(self, request):
        code = request.data.get("code")
        access_token = requests.post(
            "https://kauth.kakao.com/oauth/token",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data={
                "grant_type": "authorization_code",
                "client_id": settings.KAKAO_REST_API_KEY,
                "redirect_uri": BASE_URL,
                "code": code,
                "client_secret": settings.KAKAO_REST_API_KEY,
            },
        )

        if access_token.status_code != 200:
            return Response(
                {"status": "400", "error": "카카오 로그인 실패. 다시 시도해주세요."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        access_token = access_token.json().get("access_token")
        user_data_request = requests.get(
            "https://kapi.kakao.com/v2/user/me",
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
            },
        )
        user_datajson = user_data_request.json()
        user_data = user_datajson["kakao_account"]

        email = user_data["email"]
        nickname = user_data["profile"]["nickname"]

        data = {
            "email": email,
            "password": "aaaa1111~",
            "nickname": nickname,
            "country": "",
        }

        try:
            user = User.objects.get(email=email)
            refresh = RefreshToken.for_user(user)
            refresh["email"] = user.email
            refresh["nickname"] = user.nickname
            refresh["profile_img"] = user.profile_img.url
            return Response(
                {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
                status=status.HTTP_200_OK,
            )
        except:
            serializer = UserSerializer(data=data)

            if serializer.is_valid():
                serializer.save()
                user = User.objects.get(email=email)
                user.is_active = True
                user.set_unusable_password()
                user.save()
                refresh = RefreshToken.for_user(user)
                refresh["email"] = user.email
                refresh["nickname"] = user.nickname
                refresh["profile_img"] = user.profile_img.url
                return Response(
                    {
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                    },
                    status=status.HTTP_200_OK,
                )


class GoogleLoginView(APIView):
    def post(self, request):
        code = request.data.get("code")

        client_id = settings.SOCIAL_AUTH_GOOGLE_CLIENT_ID
        client_secret = settings.SOCIAL_AUTH_GOOGLE_CLIENT_SECRET
        redirect_uri = BASE_URL

        #  구글 API로 액세스 토큰 요청
        access_token_request = requests.post(
            "https://oauth2.googleapis.com/token",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data={
                "code": code,
                "client_id": client_id,
                "client_secret": client_secret,
                "redirect_uri": redirect_uri,
                "grant_type": "authorization_code",
                "scope": "email profile",
            },
        )

        if access_token_request.status_code != 200:
            return Response(
                {"status": "400", "error": "구글 로그인 실패. 다시 시도해주세요."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        access_token_json = access_token_request.json()
        access_token = access_token_json.get("access_token")

        # 구글 API로 사용자 정보 요청
        user_data_request = requests.get(
            "https://www.googleapis.com/oauth2/v1/userinfo",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        user_data_json = user_data_request.json()

        email = user_data_json.get("email")
        nickname = user_data_json.get("name")

        data = {
            "email": email,
            "password": "aaaa1111~",
            "nickname": nickname,
            "country": "",
        }
        try:
            user = User.objects.get(email=email)
            refresh = RefreshToken.for_user(user)
            refresh["email"] = user.email
            refresh["nickname"] = user.nickname
            refresh["profile_img"] = user.profile_img.url
            return Response(
                {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
                status=status.HTTP_200_OK,
            )
        except:
            serializer = UserSerializer(data=data)

            if serializer.is_valid():
                serializer.save()
                user = User.objects.get(email=email)
                user.is_active = True
                user.set_unusable_password()
                user.save()
                refresh = RefreshToken.for_user(user)
                refresh["email"] = user.email
                refresh["nickname"] = user.nickname
                refresh["profile_img"] = user.profile_img.url
                return Response(
                    {
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                    },
                    status=status.HTTP_200_OK,
                )
