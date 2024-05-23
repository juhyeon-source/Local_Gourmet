from rest_framework import serializers
from .models import Review, Comment

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        exclude = ("review",)

class ReviewSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    class Meta:
        model = Review
        fields = '__all__'