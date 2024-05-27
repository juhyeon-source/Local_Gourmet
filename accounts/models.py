from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

# Create your models here.
""" 회원 가입시 필요한 정보 """


class Accounts(AbstractUser):
    class GenderChoices(models.TextChoices):
        MALE = "M", "남성"
        FEMALE = "F", "여성"
        PRIVATE = "-", "선택안함"

    gender = models.CharField(
        max_length=1,
        blank=True,
        choices=GenderChoices.choices,
        default=GenderChoices.PRIVATE,  #선택안함이 기본
    )
    address = models.CharField(
        max_length=250,
    )
    phone_number = models.CharField(
        max_length=13,
        blank=True,
        validators=[RegexValidator(r"010-?\d{4}-?\d{4}$")],
        #RegexValidator을 활용해, 정규 표현식으로 나타냄
        #한국 휴대폰 번호는 무조건 010으로 시작하기 때문에 고정해둠
        #가운데, 뒷 번호의 갯수를 네개로 제한
        #/를 한번만 사용하기위해 f가 아닌 r을 사용
        #하이픈 포함 총 13자리
    )
    profile_picture = models.ImageField(
        upload_to="accounts/profile_picture/%Y/%m/%d",
        #ImageField 사용시, pip install pillow 설치 필요
        #문자열을 제외한 다른 형태의 파일을 이용 하려면 settings.py내에 MEDIA_URL 및 MEDIA_ROOT 작성 필요
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table: str = "Accounts"
