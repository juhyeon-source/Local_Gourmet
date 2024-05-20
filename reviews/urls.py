from django.urls import path
from . import views

urlpatterns = [
    path('', views.ReviewListView.as_view()),
    path('<int:review_id>/', views.ReviewDetailView.as_view()),
    path('<int:review_id>/comments/', views.CommentListView.as_view()),
    path('<int:review_id>/comments/<int:comment_id>/', views.CommentDetailView.as_view()),
]