from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator
from django.db import models

# Create your models here.
''' 회원 가입시 필요한 정보 '''


class Accounts(AbstractUser):
    class GenderChoices(models.TextChoices):
        MALE = "M", "남성"
        FEMALE = "F", "여성"

    gender = models.CharField(
        max_length=1,
        blank=True,
        choices=GenderChoices.choices,
        default=GenderChoices.FEMALE,
    )
    address = models.CharField(unique=True,
                               max_length=250,
                               choices="",
                               error_messages={
                                   "unique": "이미 등록된 주소지 입니다."
                               })
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    phone_number = models.CharField(unique=True,
                                    max_length=15,
                                    validators=[MinLengthValidator(13, "-포함 13자 이상 기입해주세요.")])

    class Meta:
        db_table: str = "Accounts"
