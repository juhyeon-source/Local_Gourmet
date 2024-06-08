from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import StoreListSerializer, StoreDetailSerializer, ImportSerializer
from .models import Store, StoreAddress
import pandas as pd


class StoreListAPIView(APIView):
    def get(self, request):
        paginator = PageNumberPagination()
        paginator.page_size = 10  # 페이지당 아이템 수를 설정
        stores = Store.objects.all()
        
        # 검색 쿼리가 있는 경우에 대한 처리
        search_query = request.query_params.get('search', None)
        if search_query:
            stores = stores.filter(store_name__icontains=search_query)
        
        result_page = paginator.paginate_queryset(stores, request)
        serializer = StoreListSerializer(result_page, many=True, context={'request': request})
        return paginator.get_paginated_response(serializer.data)


class StoreDetailAPIView(APIView):
    def get(self, request, store_id):
        stores = get_object_or_404(Store, pk=store_id)
        serializer = StoreDetailSerializer(stores)
        return Response(serializer.data, status=status.HTTP_200_OK)


class StoreImportAPIView(APIView):
    serializer_class = ImportSerializer
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        try:
            data = request.FILES
            serializer = self.serializer_class(data=data)
            if not serializer.is_valid():
                return Response({'status': False, 'message': 'Provide a valid file'}, status=status.HTTP_400_BAD_REQUEST)
            excel_file = data.get('file')
            df = pd.read_excel(excel_file, sheet_name=0)
            stores = []
            for index, row in df.iterrows():
                store_name = row['store_name']
                category = row['category']
                phone_number = row['phone_number']
                address = row['address_id']
                store = Store(store_name=store_name, category=category, phone_number=phone_number,
                              address_id=address)
                stores.append(store)
            Store.objects.bulk_create(stores)
            return Response({'status': True, 'message': 'Storedata imported successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': False, 'message': f'We could not complete the import process: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)


class AddressImportAPIView(APIView):
    serializer_class = ImportSerializer
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        try:
            data = request.FILES
            serializer = self.serializer_class(data=data)
            if not serializer.is_valid():
                return Response({'status': False, 'message': 'Provide a valid file'}, status=status.HTTP_400_BAD_REQUEST)
            excel_file = data.get('file')
            df = pd.read_excel(excel_file, sheet_name=0)
            stores = []
            for index, row in df.iterrows():
                address_si = row['address_si']
                address_gu = row['address_gu']
                address_detail = row['address_detail']
                storeaddress = StoreAddress(
                    address_si=address_si, address_gu=address_gu, address_detail=address_detail)
                stores.append(storeaddress)
            StoreAddress.objects.bulk_create(stores)
            return Response({'status': True, 'message': 'Adderssdata imported successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': False, 'message': f'We could not complete the import process: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
