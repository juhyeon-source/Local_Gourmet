from django.shortcuts import get_object_or_404
from .serializers import (ReviewListSerializer, ReviewDetailSerializer, ReviewCreateSerializer, ReviewUpdateSerializer,
                        CommentSerializer)
from .models import Review, Comment
from rest_framework.pagination import PageNumberPagination

from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly


class Pagination(PageNumberPagination):
    page_size = 5
    page_query_param = 'page_size'
    max_page_size = 10000


class ReviewListAPIView(generics.ListAPIView):
    queryset = ReviewListSerializer.get_optimized_queryset()
    serializer_class = ReviewListSerializer
    pagination_class = Pagination
    permission_classes = [AllowAny]

class ReviewCreateAPIView(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewCreateSerializer
    permission_classes = [AllowAny] # 확인하려고 이렇게 해둠. 로그인 기능 구현되면 제대로 할 예정

class ReviewDetailAPIView(generics.RetrieveAPIView):
    queryset = ReviewDetailSerializer.get_optimized_queryset()
    serializer_class = ReviewDetailSerializer
    permission_classes = [AllowAny]

class ReviewUpdateAPIView(generics.UpdateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewUpdateSerializer
    permission_classes = [AllowAny]

class ReviewDestroyAPIView(generics.DestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewListSerializer
    permission_classes = [AllowAny]


class CommentListAPIView(generics.ListAPIView):
    queryset = CommentSerializer.get_optimized_queryset()
    serializer_class = CommentSerializer
    pagination_class = Pagination
    permission_classes = [AllowAny]

class CommentCreateAPIView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        review_id = self.kwargs.get("review_pk")
        review = get_object_or_404(Review, pk=review_id)
        serializer.save(review=review)

class CommentDetailAPIView(generics.RetrieveAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [AllowAny]

class CommentUpdateAPIView(generics.UpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [AllowAny]

class CommentDestroyAPIView(generics.DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

