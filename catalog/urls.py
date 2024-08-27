from django.urls import path
from .views import ProductListCreateView, ProductRetrieveUpdateDeleteView, PopularProductsView, UpdateInventoryView, UpdateSalesCountView

urlpatterns = [
    path('products/', ProductListCreateView.as_view(), name='product-list-create'),
    path('products/<int:pk>/', ProductRetrieveUpdateDeleteView.as_view(), name='product-detail'),
    path('products/popular/', PopularProductsView.as_view(), name='popular-products'),  # New URL for popular products
    path('products/<int:pk>/update_inventory/', UpdateInventoryView.as_view(), name='update_inventory'),
    path('products/<int:pk>/update_sales/', UpdateSalesCountView.as_view(), name='update_sales'),

]
