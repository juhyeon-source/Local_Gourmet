from rest_framework import serializers
from .models import Store


class StoreListSerializer(serializers.ModelSerializer):
    # url 필드를 생성
    url = serializers.SerializerMethodField()

    class Meta:
        model = Store
        fields = ['id', 'store_name', 'url', ]

    def get_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.get_absolute_url())


class StoreDetailSerializer(serializers.ModelSerializer):
    # StoreAddress 모델의 address 속성을 참조
    address = serializers.CharField(source='address.address')

    class Meta:
        model = Store
        fields = ['id', 'store_name', 'category', 'phone_number', 'address', ]
