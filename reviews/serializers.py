from rest_framework import serializers
from rest_framework.serializers import ReadOnlyField
from .models import Review, Comment
from stores.models import Store


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        exclude = ("review",)


# class StoreSerializer(serializers.ModelSerializer):
#     name = serializers.SerializerMethodField()

#     class Meta:
#         model = Store
#         fields = ['store_name']


class ReviewSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    # store_name = StoreSerializer()

    class Meta:
        model = Review
        fields = '__all__'

    # @staticmethod
    # def get_optimized_queryset():
    #     return Review.objects.all().select_related("store_name")