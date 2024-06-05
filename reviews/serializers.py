from rest_framework import serializers
from rest_framework.serializers import ReadOnlyField
from .models import Review, Comment
from stores.models import Store
from django.contrib.auth import get_user_model

User = get_user_model()


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ['store_name', 'category']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']

# 스토어 목록이 쭉 보이고, 그 중에서 스토어 하나를 골라서 누르면 스토어 디테일 페이지가 나옴.
# 그 아래에, 해당 스토어의 리뷰 목록이 보이고 또 리뷰 하나를 클릭하면 리뷰 상세로 가게 됨.
# 그때 리뷰 상세에서 그 리뷰에 해당하는 댓글들을 보여줌.

class ReviewListSerializer(serializers.ModelSerializer):
    store = serializers.CharField(source='store.store_name')
    username = serializers.CharField(source='user.username')

    class Meta:
        model = Review
        fields = ['id', 'store', 'username', 'score']

    @staticmethod
    def get_optimized_queryset():
        return Review.objects.all().only('id', 'store_id', 'user__username', 'score').select_related('store', 'user')


class ReviewDetailSerializer(serializers.ModelSerializer):
    store = serializers.CharField(source='store.store_name')
    username = serializers.CharField(source='user.username')

    class Meta:
        model = Review
        fields = ['id', 'store_id', 'store', 'username', 'score',
                'review_content', 'image', 'created_at', 'updated_at']

    @staticmethod
    def get_optimized_queryset():
        return Review.objects.all().only('store', 'user__username').select_related('store', 'user')


class ReviewCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = ['id', 'store', 'score', 'image', 'review_content']
        read_only_fields = ['id','store']

    @staticmethod
    def get_optimized_queryset():
        return Review.objects.all().only('store', 'score').select_related('store')

    def create(self, validated_data):
        store_name = self.initial_data.get('store')
        request = self.context.get('request')
        user = request.user

        # 유저가 존재하지 않는 경우
        if not user:
            raise serializers.ValidationError('로그인한 유저여야 합니다.')
        
        # 스토어 이름으로 스토어 찾기
        store = Store.objects.filter(store_name=store_name).first()
        if not store:
            raise serializers.ValidationError('존재하지 않는 스토어입니다.')
        
        # 스토어의 address_gu와 user의 address_gu를 비교
        if user.address_gu != store.address.address_gu:
            raise serializers.ValidationError('유저와 스토어의 동네가 같지 않습니다.')

        review = Review.objects.create(user=user, store=store, **validated_data)
        return review

# update와 partial_update의 차이는 'PUT' 요청과 'PATCH' 요청의 차이라고 생각할 수 있다.
class ReviewUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['image', 'review_content']

    #instance는 업데이트할 모델 인스턴스
    #validated_data는 유효성 검사를 통과한 데이터로, 업데이트할 값들을 포함함.
    def update(self, instance, validated_data):
        #validated_data 딕셔너리의 키-값 쌍에 대해 반복하면서, instance 객체의 해당 속성(attr)을 새로운 값(value)으로 설정함.
        for attr, value in validated_data.items():
            #setattr 함수는 객체의 속성을 동적으로 설정하는 데 사용됨.
            setattr(instance, attr, value)
        
        instance.save()
        return instance

    def partial_update(self, instance, validated_data):
        # partial_update는 self.update를 반환하는데 update는 인스턴스를 업데이트하고 저장하는 로직을 포함하고 있다.
        return self.update(instance, validated_data)


class CommentSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'username', 'comment_content','created_at', 'updated_at']
        
    def get_username(self, obj):
        return obj.user.username

    @staticmethod
    def get_optimized_queryset():
        return Comment.objects.all().only('user__username').select_related('user')

