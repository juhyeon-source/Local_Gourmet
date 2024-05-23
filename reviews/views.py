from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from .serializers import ReviewSerializer, CommentSerializer
from .models import Review, Comment
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination

from rest_framework import generics
from rest_framework.generics import get_object_or_404

class ReviewListCreateAPIView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

## 바로 위 코드와 아래 코드는 같은 걸 뜻함.

# class ReviewListCreateAPIView(mixins.ListModelMixin, 
#                             mixins.CreateModelMixin, 
#                             generics.GenericAPIView):
    
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request):
#         return self.list(request)
    
#     def post(self, request):
#         return self.create(request)

class ReviewDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

# class ReviewRetrieveUpdateDestroyAPIView(mixins.RetrieveModelMixin,
#                                         mixins.UpdateModelMixin,
#                                         mixins.DestroyModelMixin,
#                                         generics.GenericAPIView):
    
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request, pk):
#         return self.retrieve(request, pk)
    
#     def put(self, request, pk):
#         return self.update(request, pk)
    
#     def delete(self, request, pk):
#         return self.destroy(request, pk)

class CommentListAPIView(generics.ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class CommentCreateAPIView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        review_id = self.kwargs.get("review_pk")
        review = get_object_or_404(Review, pk=review_id)
        serializer.save(review=review)

class CommentDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


