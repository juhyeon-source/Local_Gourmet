from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import SignupSerializer, LoginSerializer


class SignupView(CreateAPIView):
    """
    signup: 회원 가입 FBV
    """

    model = get_user_model()
    serializer_class = SignupSerializer
    permission_classes = [AllowAny]  #회원가입은 누구나 할 수 있기 때문에 AllowAny사용


class AccountLoginView(TokenObtainPairView):
    serializer_class = LoginSerializer


class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer
