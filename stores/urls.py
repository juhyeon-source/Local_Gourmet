from django.urls import path
from . import views


urlpatterns = [
    path('', views.StoreListAPIView.as_view(), name='store_list'),
    path('<int:store_id>/', views.StoreDetailAPIView.as_view(), name='store_detail'),
]