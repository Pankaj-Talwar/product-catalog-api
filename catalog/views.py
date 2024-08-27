from rest_framework.pagination import PageNumberPagination
from rest_framework import generics, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q

from .models import Product
from .serializers import ProductSerializer, InventoryUpdateSerializer

# View for listing and creating products with pagination, filtering, and sorting
class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = PageNumberPagination
    filter_backends = (filters.OrderingFilter, filters.SearchFilter)
    ordering_fields = ['price', 'sales_count']
    ordering = ['price']  # Default ordering
    
    # Apply search and filter queries
    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.query_params.get('search', None)
        name_filter = self.request.query_params.get('name', None)
        category_filter = self.request.query_params.get('category', None)

        # Apply search filtering
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

# View for retrieving, updating, and deleting a single product
class ProductRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

# View for listing popular products, ordered by sales count in descending order
class PopularProductsView(generics.ListAPIView):
    queryset = Product.objects.all().order_by('-sales_count')
    serializer_class = ProductSerializer

# View for updating inventory count of a product
class UpdateInventoryView(APIView):
    def post(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)  # Get the product by ID
            serializer = InventoryUpdateSerializer(product, data=request.data)  # Use the serializer to handle the data
            
            if serializer.is_valid():  # Validate the incoming data
                serializer.save()  # Save the changes to the product
                return Response(serializer.data, status=status.HTTP_200_OK)  # Return the updated data
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Handle validation errors
        
        except Product.DoesNotExist:  # Handle case where the product is not found
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

# View for updating sales count of a product
class UpdateSalesCountView(APIView):
    def post(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
            sales_count = request.data.get('sales_count', None)
            
            if sales_count is not None:
                product.sales_count += int(sales_count)  # Increment sales count by the provided value
                product.save()
                serializer = ProductSerializer(product)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Sales count is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
