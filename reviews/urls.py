from django.urls import path
from .views import (
    ReviewListAPIView,
    ReviewCreateAPIView,
    ReviewDetailAPIView,
    ReviewUpdateAPIView,
    ReviewDestroyAPIView,
    CommentListAPIView,
    CommentDetailAPIView,
    CommentCreateAPIView,
    CommentUpdateAPIView,
    CommentDestroyAPIView
)

urlpatterns = [
    path('list/<int:pk>/', ReviewListAPIView.as_view(), name='review-list'),
    path('create/', ReviewCreateAPIView.as_view(), name='review-create'),
    path('<int:pk>/', ReviewDetailAPIView.as_view(), name='review-detail'),
    path('<int:pk>/update/', ReviewUpdateAPIView.as_view(), name='review-update'),
    path('<int:pk>/destroy/', ReviewDestroyAPIView.as_view(), name='review-destroy'),
    path('<int:pk>/comments/', CommentListAPIView.as_view(), name='comment-list'),
    path('comments/<int:pk>/', CommentDetailAPIView.as_view(), name='comment-detail'),
    path('<int:review_pk>/comment/', CommentCreateAPIView.as_view(), name='comment-create'),
    path('comments/<int:pk>/update/', CommentUpdateAPIView.as_view(), name='comment-update'),
    path('comments/<int:pk>/destroy/', CommentDestroyAPIView.as_view(), name='comment-destroy'),
]
