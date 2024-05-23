from django.contrib.auth import get_user_model
from rest_framework import serializers

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
        )  #사용자에게 요청받은 데이터들을 의미

        user.set_password(validated_data["password"])
        #password는 암호화 되어야 하기 때문에, 다른것 들과는 다르게 set_password를 이용
        user.save()  #User.objects.create으로 받아온 내용들을 저장
        return user

    class Meta:
        model = User
        fields = [
            "pk",
            "username",
            "password",
            "gender",
            "phone_number",
            "address",
            "profile_picture",
        ]
        #조건
