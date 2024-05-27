from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from .serializers import ReviewSerializer, CommentSerializer
from .models import Review, Comment
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

class ReviewListView(APIView):

    def get(self, request):
        reviews = Review.objects.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def post(self, request):
        self.permission_classes = [IsAuthenticated]
        self.check_permissions(request)
        serializer = ReviewSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)



class ReviewDetailView(APIView):

    def get(self, request, review_id):
        review = get_object_or_404(Review, pk=review_id)
        serializer = ReviewSerializer(review)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def put(self, request, review_id):
        self.permission_classes = [IsAuthenticated]
        self.check_permissions(request)
        review = get_object_or_404(Review, pk=review_id)

        if request.user != review.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
        serializer = ReviewSerializer(review, data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)


    def delete(self, request, review_id):
        self.permission_classes = [IsAuthenticated]
        self.check_permissions(request)
        review = get_object_or_404(Review, pk=review_id)

        if request.user != review.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
        review.delete()
        data = {"delete": f"Review({review_id}) is deleted."}
        return Response(data, status=status.HTTP_204_NO_CONTENT)



class CommentListView(APIView):

    def get(self, request, review_id):
        comments = Comment.objects.filter(review_id=review_id)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status = status.HTTP_200_OK)


    def post(self, request, review_id):
        self.permission_classes = [IsAuthenticated]
        self.check_permissions(request)
        serializer = CommentSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)



class CommentDetailView(APIView):

    def put(self, request, review_id, comment_id):
        self.permission_classes = [IsAuthenticated]
        self.check_permissions(request)
        comment = get_object_or_404(Comment, pk=comment_id)
        serializer = CommentSerializer(comment, data=request.data, partial=True)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)


    def delete(self, request, review_id, comment_id):
        self.permission_classes = [IsAuthenticated]
        self.check_permissions(request)
        comment = get_object_or_404(Comment, pk=comment_id)

        if request.user != comment.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
        comment.delete()
        data = {"delete": f"Comment({comment_id}) is deleted."}
        return Response(data, status=status.HTTP_204_NO_CONTENT)

