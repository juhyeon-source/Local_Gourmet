from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from stores.models import Store


class Accounts(AbstractUser):
    class GenderChoices(models.TextChoices):
        MALE = "M", "남성"
        FEMALE = "F", "여성"
        PRIVATE = "-", "선택안함"

    gender = models.CharField(
        max_length=1,
        blank=True,
        choices=GenderChoices.choices,
        default=GenderChoices.PRIVATE,  # 선택안함이 기본
    )
    address_si = models.CharField(max_length=50)
    address_gu = models.CharField(max_length=30, default="default_value")
    address_detail = models.CharField(max_length=250)

    phone_number = models.CharField(
        max_length=13,
        blank=True,
        validators=[RegexValidator(r"010-?\d{4}-?\d{4}$")],
        # RegexValidator을 활용해, 정규 표현식으로 나타냄
        # 한국 휴대폰 번호는 무조건 010으로 시작하기 때문에 고정해둠
        # 가운데, 뒷 번호의 갯수를 네개로 제한
        # /를 한번만 사용하기위해 f가 아닌 r을 사용
        # 하이픈 포함 총 13자리
    )
    profile_picture = models.ImageField(
        upload_to="accounts/profile_picture/%Y/%m/%d",
        # ImageField 사용시, pip install pillow 설치 필요
        # 문자열을 제외한 다른 형태의 파일을 이용 하려면 settings.py내에 MEDIA_URL 및 MEDIA_ROOT 작성 필요
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def name(self):
        return f"{self.first_name} {self.last_name}".strip()

    class Meta:
        db_table: str = "Accounts"


class StoreAddress(models.Model):
    address_si = models.CharField(max_length=10)
    address_gu = models.CharField(max_length=10)
    address_detail = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.address_si} {self.address_gu} {self.address_detail}"


class Bookmark(models.Model):
    user = models.ForeignKey(
        Accounts, on_delete=models.CASCADE, related_name="bookmarks"
    )
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    # user과 store 모두 1:N 이기 때문에 FK를 사용
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "store")
        # user와 store 사이에 중복이 발생 하면 안되기 때문에 unique_together 사용
