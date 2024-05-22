from rest_framework import serializers
from .models import Review, Comment

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = (
            'id',
            'store',
            'user',
            'username',
            'store_name',
            'created_at',
            'updated_at',
        )


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = (
            'id',
            'review',
            'user',
            'created_at',
            'updated_at',
        )