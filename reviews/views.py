from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from .serializers import ReviewSerializer, CommentSerializer
from .models import Review, Comment
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination


# 주소 인증은 잠시 빼두고 진행! 아직 할 수 있는 게 없다 ..
# 이미지 업로드 조건 : 메뉴판 사진, 주문한 음식 사진
# 이거는 .. 이미지 인식을 하기엔 빡세니깐 그냥 프론트에서 적어만 놓을까?
# generic으로 한 번 해보기

class ReviewListView(APIView):

    def get(self, request):
        paginator = PageNumberPagination()
        paginator.page_size = 10
        reviews = Review.objects.all()
        result_page = paginator.paginate_queryset(reviews, request)
        serializer = ReviewSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data, status=status.HTTP_200_OK)


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

# 수정은 기한 딱 하루만 하게 해야함.
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

# 프론트딴에서 정말 삭제하시겠냐고 팝업창 띄우기
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

