from django.urls import path
from . import views


urlpatterns = [
    path('', views.StoreListAPIView.as_view(), name='store_list'),
    path('<int:store_id>/', views.StoreDetailAPIView.as_view(), name='store_detail'),
    path('storeimport/', views.StoreImportAPIView.as_view(), name='store_import'),
    path('addressimport/', views.AddressImportAPIView.as_view(), name='address_import'),
]