from rest_framework.serializers import ModelSerializer
from django.contrib.auth import get_user_model


class AccountSerializer(ModelSerializer):
    class Meta:
        '''
        error_messages = None
        '''
        model = get_user_model()
        fields = [
            "id",
            "username",
            "password",
            "email",
            "address",
            "created",
        ]

        error_message = {
            "password":
                {"same_password": "변경하려는 비밀번호는 이전 비밀번호와 다르게 지정해야 합니다."}

        }

    def validate_password(self, password):
        len_password = len(password)
        err_msg = self.Meta.error_messages.get("password")
        return password
