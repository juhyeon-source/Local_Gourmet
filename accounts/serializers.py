from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import NotFound
from rest_framework.generics import get_object_or_404
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from accounts.models import Bookmark

User = get_user_model()


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data["username"],
            gender=validated_data["gender"],
            phone_number=validated_data["phone_number"],
            address=validated_data["address"],
            profile_picture=validated_data["profile_picture"],
        )  # 왼쪽 : models.py에 정의되어있는 값과 동일한 이름으로 작성필요
        # 오른쪽 : 사용자에게 요청받은 데이터들을 의미

        user.set_password(validated_data["password"])
        # password는 암호화 되어야 하기 때문에, 다른것 들과는 다르게 set_password를 이용
        user.save()  # User.objects.create으로 받아온 내용들을 저장
        return user

    class Meta:
        model = User
        # 위에서 정의한 get_user_model()을 의미
        fields = [
            "pk",
            "username",
            "password",
            "gender",
            "phone_number",
            "address",
            "profile_picture",
        ]


class UserSerializer(serializers.ModelSerializer):
    """회원가입 페이지"""

    # 이메일 중복 검증
    email = serializers.EmailField(required=True, validators=[UniqueValidator])

    username = serializers.CharField(required=True, validators=[UniqueValidator])

    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )

    class Meta:
        model = User
        fields = ("username", "password", "email")

    def create(self, validated_data):
        user = super().create(validated_data)
        password = user.password
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        user = get_object_or_404(User, username=attrs[self.username_field])

        if not check_password(attrs["password"], user.password):
            raise NotFound(
                "사용자를 찾을 수 없습니다. 로그인 정보를 확인 해주세요."
            )  # 404 Not Found

        else:
            # 기본 동작을 실행하고 반환된 데이터를 저장.
            data = super().validate(attrs)
            return data

    @classmethod
    def get_token(cls, user):
        #classmethod를 사용하려면 무조건 cls(class)를 작성해주어야 함
        token = super().get_token(user)
        # token['email'] = user.email
        # 이메일 인증시 사용 예정
        token["username"] = user.username
        return token


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["pk", "username", "gender", "phone_number", "address", "profile_picture"]


class BookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmark
        fields = ["id", "store", "created_at", "updated_at"]
