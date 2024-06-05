import requests
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView, ListAPIView, DestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import viewsets, status

# from allauth.socialaccount.providers.kakao import views as kakao_view

from .models import Bookmark
from .serializers import (
    SignupSerializer,
    LoginSerializer,
    ProfileSerializer,
    BookmarkSerializer,
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
        response = super().delete(request, *args, **kwargs)
        return Response(
            {"message": "계정이 성공적으로 삭제되었습니다."},
            status=response.status_code,
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


# 소셜 로그인


class KakaoLogin(APIView):
    def post(self, request):
        client_id = KAKAO_REST_API_KEY

        received_code = request.data.get("code")  # 받은 ?code='' 값
        code_value = received_code.split("?code=")[-1]  # 코드 값만 추출
        print(code_value)

        kakao_token = requests.post(
            "https://kauth.kakao.com/oauth/token",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data={
                "grant_type": "authorization_code",
                "client_id": client_id,
                "redirect_uri": f"{REDIRECT_URL}/redirect.html",
                "code": code_value,
            },
        )
        print(kakao_token.json)  # access_token 발급 완료

        access_token = kakao_token.json()["access_token"]
        refresh_token = kakao_token.json()["refresh_token"]

        token_data = {"access": access_token, "refresh": refresh_token}
        # access_token 으로 사용자 정보 가져오기
        user_data = requests.get(
            "https://kapi.kakao.com/v2/user/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        # 이메일, 닉네임, 프로필 사진 가져오기
        user_data = user_data.json()

        kakao_account = user_data.get("kakao_account")
        user_email = kakao_account.get("email")
        user_nickname = kakao_account.get("profile")["nickname"]
        user_img = kakao_account.get("profile")["profile_image_url"]

        try:
            # 기존에 가입된 유저나 소셜 로그인 유저가 존재하면 로그인
            user = User.objects.get(email=user_email)
            social_user = SocialAccount.objects.filter(uid=user_email).first()

            # 동일한 이메일의 유저가 있지만, 소셜 계정이 아닐 때
            if social_user is None:
                return Response(
                    {"error": "소셜 계정이 아닌 이미 존재하는 이메일입니다."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # 소셜 계정이 카카오가 아닌 다른 소셜 계정으로 가입했을 때
            if social_user.provider != "kakao":
                return Response(
                    {"error": "다른 소셜 계정으로 가입되어 있습니다."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # 소셜 로그인 사용자의 경우
            if social_user:
                # 사용자의 비밀번호 없이 로그인 가능한 JWT 토큰 생성
                print(social_user)
                refresh = RefreshToken.for_user(user)
                return Response(
                    {
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                        "provider": social_user.provider,
                        "is_admin": user.is_admin,
                        "msg": "로그인 성공",
                    },
                    status=status.HTTP_200_OK,
                )

        except User.DoesNotExist:
            # 기존에 가입된 유저가 없으면 유저 모델에 생성후 소셜어카운트에 포함시키는 로직
            new_user = User.objects.create(
                email=user_email,
                nickname=user_nickname,
                profile_img=user_img,
            )

            # 소셜 계정도 생성하고 포함시키기
            SocialAccount.objects.create(
                user_id=new_user.id,
                uid=new_user.email,
                provider="kakao",
            )

            # 새로운 사용자에 대한 JWT 토큰 생성
            refresh = RefreshToken.for_user(new_user)

            return Response(
                {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                    "is_admin": user.is_admin,
                    "msg": "회원가입 성공",
                },
                status=status.HTTP_201_CREATED,
            )


class GithubLogin(APIView):
    def post(self, request):
        client_id = SOCIAL_AUTH_GITHUB_CLIENT_ID
        client_secret = SOCIAL_AUTH_GITHUB_SECRET

        received_code = request.data.get("code")
        code_value = received_code.split("?code=")[-1]

        """토큰"""
        github_token = requests.post(
            f"https://github.com/login/oauth/access_token",
            headers={"Accept": "application/json"},
            data={
                "client_id": client_id,
                "client_secret": client_secret,
                "redirect_url": f"{REDIRECT_URL}/redirectGit.html",
                "code": code_value,
            },
        )

        access_token = github_token.json()["access_token"]

        token_data = {"access": access_token, "auth": "github"}

        """유저 데이터"""
        user_data = requests.get(
            "https://api.github.com/user",
            headers={
                "Authorization": f"Bearer {access_token}",
                "Accept": "application/json",
            },
        )

        user_data = user_data.json()

        """유저 이메일"""
        user_emails = requests.get(
            "https://api.github.com/user/emails",
            headers={
                "Authorization": f"Bearer {access_token}",
                "Accept": "application/json",
            },
        )
        user_emails = user_emails.json()

        try:
            user = User.objects.get(email=user_emails[0]["email"])
            print(user)
            social_user = SocialAccount.objects.filter(
                uid=user_emails[0]["email"]
            ).first()

            # if social_user:
            #     refresh = RefreshToken.for_user(user)

            #     return Response({'refresh': str(refresh), 'access': str(refresh.access_token), "msg": "로그인 성공"}, status=status.HTTP_200_OK)

            if social_user is None:
                return Response(
                    {"error": "소셜 계정이 아닌 이미 존재하는 이메일입니다."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if social_user.provider != "github":
                return Response(
                    {"error": "다른 소셜 계정으로 가입되어 있습니다."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if social_user:
                refresh = RefreshToken.for_user(user)

                return Response(
                    {
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                        "provider": social_user.provider,
                        "is_admin": user.is_admin,
                        "msg": "로그인 성공",
                    },
                    status=status.HTTP_200_OK,
                )

        except User.DoesNotExist:
            new_user = User.objects.create(
                nickname=user_data.get("login"),
                email=user_emails[0]["email"],
                profile_img=user_data.get("avatar_url"),
            )
            SocialAccount.objects.create(
                user_id=new_user.id,
                uid=new_user.email,
                provider="github",
            )

            refresh = RefreshToken.for_user(new_user)

            return Response(
                {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                    "is_admin": user.is_admin,
                    "msg": "회원가입 성공",
                },
                status=status.HTTP_201_CREATED,
            )
