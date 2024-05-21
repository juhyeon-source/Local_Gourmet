from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from .serializers import SignupSerializer


class SignupView(CreateAPIView):
    """
    signup: 회원 가입 FBV
    """

    model = get_user_model()
    serializer_class = SignupSerializer
    permission_classes = [AllowAny]


class AccountLogInView(APIView):
    def login(self, request):
        pass


def logout(self, request):
    pass


class AccountDetailView(APIView):
    pass
