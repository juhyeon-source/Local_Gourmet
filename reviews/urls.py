from django.urls import path
from .views import (
    ReviewListAPIView,
    ReviewCreateAPIView,
    ReviewDetailAPIView,
    ReviewUpdateAPIView,
    ReviewDestroyAPIView,
    CommentListAPIView,
    CommentCreateAPIView,
    CommentDetailAPIView,
    CommentUpdateAPIView,
    CommentDestroyAPIView
)

urlpatterns = [
    path('', ReviewListAPIView.as_view()),
    path('create/', ReviewCreateAPIView.as_view()),
    path('<int:pk>/', ReviewDetailAPIView.as_view()),
    path('<int:pk>/update/', ReviewUpdateAPIView.as_view()),
    path('<int:pk>/destroy/', ReviewDestroyAPIView.as_view()),
    path('<int:pk>/comments/', CommentListAPIView.as_view()),
    path('<int:review_pk>/comment/', CommentCreateAPIView.as_view()),
    path('comments/<int:pk>/', CommentDetailAPIView.as_view()),
    path('comments/<int:pk>/update/', CommentUpdateAPIView.as_view()),
    path('comments/<int:pk>/destroy/', CommentDestroyAPIView.as_view()),
]
