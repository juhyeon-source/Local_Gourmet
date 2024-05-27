from django.db import models
from django.urls import reverse


class StoreAddress(models.Model):
    address_si = models.CharField(max_length=10)
    address_gu = models.CharField(max_length=10)
    address_detail = models.CharField(max_length=100)
    
    def __str__(self):
        return f'{self.address_si} {self.address_gu} {self.address_detail}'
    
class Store(models.Model):
    CATEGORY_CHOICES = (
        ("Korean", "한식"),
        ("Chinese", "중식"),
        ("Japanese", "일식"),
        ("Western", "양식"),
        ("Dessert", "디저트"),
        ("Pub", "주점"),
        ("FastFood", "패스트푸드"),
        ("Other", "기타"),
    )
    store_name = models.CharField(max_length=100)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    phone_number = models.CharField(max_length=13)
    address = models.OneToOneField(StoreAddress, on_delete=models.CASCADE)

    # 'store_detail' Views에 URL을 반환
    def get_absolute_url(self):
        return reverse('store_detail', args=[str(self.id)])
