from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import StoreListSerializer, StoreDetailSerializer
from .models import Store
from rest_framework.pagination import PageNumberPagination


class StoreListAPIView(APIView):
    def get(self, request):
        paginator = PageNumberPagination()
        paginator.page_size = 10  # 페이지당 아이템 수를 설정
        stores = Store.objects.all()
        result_page = paginator.paginate_queryset(stores, request)
        serializer = StoreListSerializer(result_page, many=True, context={'request': request})
        return paginator.get_paginated_response(serializer.data)


class StoreDetailAPIView(APIView):
    def get(self, request, store_id):
        stores = get_object_or_404(Store, pk=store_id)
        serializer = StoreDetailSerializer(stores)
        return Response(serializer.data, status=status.HTTP_200_OK)
