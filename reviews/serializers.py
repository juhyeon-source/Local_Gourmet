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


class ReviewListSerializer(serializers.ModelSerializer):
    store = StoreSerializer()
    username = serializers.CharField(source='user.username')

    class Meta:
        model = Review
        fields = ['id', 'store', 'username', 'score']

    @staticmethod
    def get_optimized_queryset():
        return Review.objects.all().only('id', 'store_id', 'user__username', 'score').select_related('store', 'user')


class ReviewDetailSerializer(serializers.ModelSerializer):
    store = StoreSerializer()
    username = serializers.CharField(source='user.username')

    class Meta:
        model = Review
        fields = ['id', 'store', 'username', 'score',
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
        store = Store.objects.filter(store_name=store_name).first()
        if not store:
            raise serializers.ValidationError('이런 스토어는 없습니다!')
        review = Review.objects.create(
            user=user, store=store, **validated_data)
        return review


class ReviewUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['image', 'review_content']

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance

    def partial_update(self, instance, validated_data):
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

