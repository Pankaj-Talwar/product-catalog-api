from rest_framework.pagination import PageNumberPagination
from rest_framework import generics, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q

from .models import Product
from .serializers import ProductSerializer, InventoryUpdateSerializer

class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = PageNumberPagination
    filter_backends = (filters.OrderingFilter, filters.SearchFilter)
    ordering_fields = ['price', 'sales_count']
    ordering = ['price']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.query_params.get('search', None)
        name_filter = self.request.query_params.get('name', None)
        category_filter = self.request.query_params.get('category', None)

        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(category__icontains=search_query)
            )
        
        if name_filter:
            queryset = queryset.filter(name__icontains=name_filter)

        if category_filter:
            queryset = queryset.filter(category__icontains=category_filter)

        return queryset

class ProductRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class PopularProductsView(generics.ListAPIView):
    queryset = Product.objects.all().order_by('-sales_count')
    serializer_class = ProductSerializer

class UpdateInventoryView(APIView):
    def post(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
            serializer = InventoryUpdateSerializer(product, data=request.data)
            
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

class UpdateSalesCountView(APIView):
    def post(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
            sales_count = request.data.get('sales_count')
            
            if sales_count is not None:
                try:
                    sales_count = int(sales_count)
                except ValueError:
                    return Response({'error': 'Sales count must be an integer'}, status=status.HTTP_400_BAD_REQUEST)

                if sales_count < 0:
                    return Response({'error': 'Sales count cannot be negative'}, status=status.HTTP_400_BAD_REQUEST)

                product.sales_count += sales_count
                product.save()
                serializer = ProductSerializer(product)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Sales count is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
