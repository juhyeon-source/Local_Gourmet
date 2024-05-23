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
        )
        user.set_password(validated_data["password"])
        user.save()
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
