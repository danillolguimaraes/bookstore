from django.test import TestCase
from product.models.product import Product, Category
from product.serializers.product_serializer import ProductSerializer


class TestProductSerializer(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            title="Tech",
            slug="tech",
            description="Technology related items",
            active=True,
        )

    def test_product_serializer(self):
        product = Product.objects.create(
            title="Mouse", description="Wireless mouse", price=100, active=True
        )
        product.category.add(self.category)

        serializer = ProductSerializer(product)
        expected_data = {
            "id": product.id,
            "title": "Mouse",
            "description": "Wireless mouse",
            "price": 100,
            "active": True,
            "category": [
                {
                    "id": self.category.id,
                    "title": "Tech",
                    "slug": "tech",
                    "description": "Technology related items",
                    "active": True,
                }
            ],
        }

        self.assertEqual(serializer.data, expected_data)
