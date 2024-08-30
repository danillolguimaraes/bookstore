from django.test import TestCase
from product.models.category import Category
from product.serializers.category_serializer import CategorySerializer


class TestCategorySerializer(TestCase):
    def test_category_serializer(self):
        category = Category.objects.create(
            title="Tech",
            slug="tech",
            description="Technology related items",
            active=True,
        )

        serializer = CategorySerializer(category)
        expected_data = {
            "id": category.id,
            "title": "Tech",
            "slug": "tech",
            "description": "Technology related items",
            "active": True,
        }

        self.assertEqual(serializer.data, expected_data)
