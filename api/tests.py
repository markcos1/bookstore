from decimal import Decimal
from django.test import TestCase
from .models import Category, Product, Order
from .serializers import CategorySerializer, ProductSerializer, OrderSerializer


class CategorySerializerTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(title="Eletrônicos")
        self.serializer = CategorySerializer(instance=self.category)

    def test_category_serialization(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), {'id', 'title'})
        self.assertEqual(data['title'], "Eletrônicos")

    def test_category_invalid_data(self):
        serializer = CategorySerializer(data={'title': ''})
        self.assertFalse(serializer.is_valid())
        self.assertIn('title', serializer.errors)


class ProductSerializerTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(title="Livros")
        self.product = Product.objects.create(
            name="Clean Code",
            price=Decimal("120.50"),
            active=True,
            category=self.category
        )

    def test_product_serialization(self):
        serializer = ProductSerializer(instance=self.product)
        data = serializer.data
        self.assertEqual(data['name'], "Clean Code")
        self.assertEqual(data['price'], "120.50")
        self.assertEqual(data['category']['title'], "Livros")

    def test_product_deserialization_valid(self):
        payload = {
            "name": "Python Fluente",
            "price": "150.00",
            "active": True,
            "category_id": self.category.id
        }
        serializer = ProductSerializer(data=payload)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        product = serializer.save()
        self.assertEqual(product.category, self.category)

    def test_product_negative_price_invalid(self):
        payload = {
            "name": "Produto Inválido",
            "price": "-10.00",
            "category_id": self.category.id
        }
        serializer = ProductSerializer(data=payload)
        self.assertFalse(serializer.is_valid())
        self.assertIn('price', serializer.errors)


class OrderSerializerTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(title="Periféricos")
        self.prod1 = Product.objects.create(
            name="Teclado Mecânico", price=Decimal("350.00"), category=self.category
        )
        self.prod2 = Product.objects.create(
            name="Mouse Gamer", price=Decimal("200.00"), category=self.category
        )

    def test_order_creation_and_serialization(self):
        payload = {
            "product_ids": [self.prod1.id, self.prod2.id]
        }
        serializer = OrderSerializer(data=payload)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        order = serializer.save()

        self.assertEqual(order.products.count(), 2)
        
        output_data = OrderSerializer(instance=order).data
        self.assertEqual(len(output_data['products']), 2)
        self.assertIn('created_at', output_data)

    def test_order_empty_products_invalid(self):
        serializer = OrderSerializer(data={"product_ids": []})
        self.assertFalse(serializer.is_valid())
        self.assertIn("product_ids", serializer.errors)

