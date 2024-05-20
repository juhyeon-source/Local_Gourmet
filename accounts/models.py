from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
''' 회원 가입시 필요한 정보 '''


class Accounts(AbstractUser):
    username = models.CharField(unique=True,
                                max_length=30,
                                error_messages={
                                    "unique": "이미 등록된 계정명입니다.",
                                })
    email = models.EmailField(unique=True,
                              error_messages={
                                  "unique": "이미 등록된 이메일 주소입니다.",
                              }
                              )
    address = models.CharField(unique=True,
                               max_length=250,
                               error_messages={
                                   "unique": "이미 등록된 주소지 입니다."
                               })

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table: str = "Accounts"
