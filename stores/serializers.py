from rest_framework import serializers
from .models import Store, StoreAddress


class StoreAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreAddress
        fields = ['address_si', 'address_gu', 'address_detail']
        
        
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
    # StoreAddress의 Fields을 가져옴
    address = StoreAddressSerializer()

    class Meta:
        model = Store
        fields = ['id', 'store_name', 'category', 'phone_number', 'address']
        
class ImportSerializer(serializers.Serializer):
    file = serializers.FileField()
