from django.test import TestCase
from api.models import Category, Product, Order
from api.serializers import CategorySerializer, ProductSerializer, OrderSerializer

class BookstoreSerializersTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(title="Livros de Ficção")
        self.product = Product.objects.create(
            name="O Senhor dos Anéis",
            price=79.90,
            category=self.category
        )

    def test_category_serializer_valid_data(self):
        data = {"title": "Biografias"}
        serializer = CategorySerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_product_serializer_accepts_valid_data(self):
        data = {
            "name": "O Hobbit",
            "price": "49.90",
            "category_id": self.category.id
        }
        serializer = ProductSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_product_serializer_requires_fields(self):
        data = {
            "price": "49.90",
            "category_id": self.category.id
        }
        serializer = ProductSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("name", serializer.errors)

    def test_product_serializer_rejects_zero_or_negative_price(self):
        data = {
            "name": "Livro com erro de preço",
            "price": "0.00",
            "category_id": self.category.id
        }
        serializer = ProductSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("price", serializer.errors)

    def test_order_serializer_creates_order_with_products(self):
        data = {
            "product_ids": [self.product.id]
        }
        serializer = OrderSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        
        order = serializer.save()
        self.assertEqual(order.products.count(), 1)
        self.assertEqual(order.products.first().name, "O Senhor dos Anéis")

