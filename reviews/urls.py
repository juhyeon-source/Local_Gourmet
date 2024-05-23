from django.urls import path
from .views import (
    ReviewListCreateAPIView,
    ReviewDetailAPIView,
    CommentListAPIView,
    CommentCreateAPIView,
    CommentDetailAPIView
)

urlpatterns = [
    path('', ReviewListCreateAPIView.as_view()),
    path('<int:pk>/', ReviewDetailAPIView.as_view()),
    path('<int:pk>/comments/', CommentListAPIView.as_view()),
    path('<int:review_pk>/comment/', CommentCreateAPIView.as_view()),
    path('comments/<int:pk>/', CommentDetailAPIView.as_view()),
]
