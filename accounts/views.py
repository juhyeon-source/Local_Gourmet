from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView, ListAPIView, DestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import viewsets

from .models import Bookmark
from .serializers import (
    SignupSerializer,
    LoginSerializer,
    ProfileSerializer,
    BookmarkSerializer,
)


class SignupView(CreateAPIView):
    """
    signup: 회원 가입 FBV
    """

    model = get_user_model()
    serializer_class = SignupSerializer
    permission_classes = [AllowAny]  # 회원가입은 누구나 할 수 있기 때문에 AllowAny사용


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
    # FIXME: permission
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
