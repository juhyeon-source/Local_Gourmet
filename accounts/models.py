from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

# Create your models here.
""" 회원 가입시 필요한 정보 """


class Accounts(AbstractUser):
    class GenderChoices(models.TextChoices):
        MALE = "M", "남성"
        FEMALE = "F", "여성"

    gender = models.CharField(
        max_length=1,
        blank=True,
        choices=GenderChoices.choices,
    )
    address = models.CharField(
        max_length=250,
    )
    phone_number = models.CharField(
        max_length=13,
        blank=True,
        validators=[RegexValidator(r"010-?\d{4}-?\d{4}$")],
    )
    profile_picture = models.ImageField(
        upload_to="accounts/profile_picture/%Y/%m/%d",
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table: str = "Accounts"
