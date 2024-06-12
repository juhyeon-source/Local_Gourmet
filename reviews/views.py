from django.shortcuts import get_object_or_404

from reviews.permissions import IsAuthor
from .serializers import (ReviewListSerializer, ReviewDetailSerializer, ReviewCreateSerializer, ReviewUpdateSerializer,
                          CommentSerializer)
from .models import Review, Comment
from rest_framework.pagination import PageNumberPagination

from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated

from rest_framework.parsers import MultiPartParser, FormParser


class Pagination(PageNumberPagination):
    page_size = 5
    page_query_param = 'page_size'
    max_page_size = 10000


class ReviewListAPIView(generics.ListAPIView):
    queryset = ReviewListSerializer.get_optimized_queryset()
    serializer_class = ReviewListSerializer
    pagination_class = Pagination
    permission_classes = [AllowAny]

    def get_queryset(self):
        store_id = self.kwargs['pk']
        return ReviewListSerializer.get_optimized_queryset().filter(store_id=store_id)


class ReviewCreateAPIView(generics.CreateAPIView):
    # queryset = ReviewCreateSerializer.get_optimized_queryset()
    queryset = Review.objects.all()
    serializer_class = ReviewCreateSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]


class ReviewDetailAPIView(generics.RetrieveAPIView):
    queryset = ReviewDetailSerializer.get_optimized_queryset()
    serializer_class = ReviewDetailSerializer
    permission_classes = [AllowAny]


class ReviewUpdateAPIView(generics.UpdateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer(self, *args, **kwargs):
        kwargs['partial'] = True  # partial=True 설정
        return super().get_serializer(*args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        return Review.objects.filter(user=user)


class ReviewDestroyAPIView(generics.DestroyAPIView):
    queryset = ReviewListSerializer.get_optimized_queryset()
    serializer_class = ReviewListSerializer
    permission_classes = [IsAuthenticated, IsAuthor]


class CommentListAPIView(generics.ListAPIView):
    queryset = CommentSerializer.get_optimized_queryset()
    serializer_class = CommentSerializer
    pagination_class = Pagination
    permission_classes = [AllowAny]

    def get_queryset(self):
        review_id = self.kwargs['pk']
        return CommentSerializer.get_optimized_queryset().filter(review_id=review_id)


class CommentDetailAPIView(generics.RetrieveAPIView):
    queryset = CommentSerializer.get_optimized_queryset()
    serializer_class = CommentSerializer
    pagination_class = Pagination
    permission_classes = [AllowAny]

    def get_queryset(self):
        comment_id = self.kwargs['pk']
        return CommentSerializer.get_optimized_queryset().filter(id=comment_id)


class CommentCreateAPIView(generics.CreateAPIView):
    queryset = CommentSerializer.get_optimized_queryset()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        review_id = self.kwargs.get("review_pk")
        review = get_object_or_404(Review, pk=review_id)
        serializer.save(review=review, user=self.request.user)


class CommentUpdateAPIView(generics.UpdateAPIView):
    queryset = CommentSerializer.get_optimized_queryset()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsAuthor]


class CommentDestroyAPIView(generics.DestroyAPIView):
    queryset = CommentSerializer.get_optimized_queryset()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsAuthor]
