from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Product

class ProductAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Create initial products for testing
        self.product1 = Product.objects.create(
            name='iPhone 15',
            description='Latest Apple iPhone',
            price=84000.00,
            inventory_count=50,
            category='Electronics',
            sales_count=160
        )
        self.product2 = Product.objects.create(
            name='Laptop',
            description='Latest Laptop',
            price=54000.00,
            inventory_count=70,
            category='Electronics',
            sales_count=210
        )

    def test_get_products(self):
        response = self.client.get(reverse('product-list-create'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)  # Ensure we get the correct count of products
        self.assertEqual(len(response.data['results']), 2)  # Ensure the correct number of products are returned

    def test_create_product(self):
        data = {
            'name': 'New Laptop',
            'description': 'A new high-end laptop',
            'price': 120000.00,
            'inventory_count': 30,
            'category': 'Electronics',
            'sales_count': 0
        }
        response = self.client.post(reverse('product-list-create'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 3)  # Ensure a new product is created
        self.assertEqual(Product.objects.get(pk=response.data['id']).name, 'New Laptop')

    def test_update_inventory(self):
        data = {'inventory_count': 80}
        response = self.client.post(reverse('update_inventory', kwargs={'pk': self.product1.id}), data, format='json')
        self.product1.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.product1.inventory_count, 80)  # Check if inventory count is updated correctly

    def test_update_sales_count(self):
        data = {'sales_count': 50}
        response = self.client.post(reverse('update_sales', kwargs={'pk': self.product1.id}), data, format='json')
        self.product1.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.product1.sales_count, 210)  # Ensure sales count is incremented correctly

    def test_popular_products(self):
        response = self.client.get(reverse('popular-products'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)  # Ensure both products are returned
        # Check if products are sorted by sales_count in descending order
        self.assertGreater(response.data['results'][0]['sales_count'], response.data['results'][1]['sales_count'])

    def test_filter_by_name(self):
        response = self.client.get(reverse('product-list-create') + '?name=iPhone 15')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)  # Ensure filtering by name works
        self.assertEqual(response.data['results'][0]['name'], 'iPhone 15')

    def test_filter_by_category(self):
        response = self.client.get(reverse('product-list-create') + '?category=Electronics')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)  # Ensure filtering by category works

    def test_ordering_by_sales_count(self):
        response = self.client.get(reverse('product-list-create') + '?ordering=-sales_count')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)  # Ensure we get both products
        # Check if products are ordered by sales_count in descending order
        self.assertGreater(response.data['results'][0]['sales_count'], response.data['results'][1]['sales_count'])
