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
    username = serializers.CharField(read_only=True)
    class Meta:
        model = User
        fields = ['username']

class ReviewListSerializer(serializers.ModelSerializer):
    store = StoreSerializer()
    username = UserSerializer(source='user_id')

    class Meta:
        model = Review
        fields = ['id', 'store', 'username', 'score']

    @staticmethod
    def get_optimized_queryset():
        return Review.objects.all().only('store', 'user', 'score').select_related('store', 'user')
    

class ReviewDetailSerializer(serializers.ModelSerializer):
    store = StoreSerializer()
    username = UserSerializer(source='user_id')

    class Meta:
        model = Review
        fields = ['id', 'store', 'username', 'score', 'review_content', 'image', 'created_at', 'updated_at']

    @staticmethod
    def get_optimized_queryset():
        return Review.objects.all().only('store', 'user').select_related('store', 'user')
    

class StoreCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ['store_name', 'address']

class ReviewCreateSerializer(serializers.ModelSerializer):
    store = StoreCreateSerializer()

    class Meta:
        model = Review
        fields = ['store', 'score', 'image', 'review_content']

    @staticmethod
    def get_optimized_queryset():
        return Review.objects.all().only('store', 'score').select_related('store')
    
    def create(self, validated_data):
        store_data = validated_data.pop('store')
        request = self.context.get('request')
        user = request.user
        store = Store.objects.create(**store_data)
        review = Review.objects.create(store=store, user=user, **validated_data)
        return review
    
class ReviewUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['image', 'review_content']


class CommentSerializer(serializers.ModelSerializer):
    username = UserSerializer(source='user_id')

    class Meta:
        model = Comment
        fields = ['id', 'username', 'comment_content' ,'created_at', 'updated_at']

    @staticmethod
    def get_optimized_queryset():
        return Comment.objects.all().only('user').select_related('user')
