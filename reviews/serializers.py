from rest_framework import serializers
from .models import Review, Comment

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = (
            'id',
            # 'user_id',
            # 'store_id',
            # 'store_name',
            'created_at',
            'updated_at',
        )


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = (
            'id',
            'review_id',
            # 'user_id',
            'created_at',
            'updated_at',
        )