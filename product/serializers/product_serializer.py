from rest_framework import serializers
from product.models.product import Product, Category
from product.serializers.category_serializer import CategorySerializer


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True, many=True)
    categories_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), write_only=True, many=True
    )

    class Meta:
        model = Product
        fields = [
            "id",
            "title",
            "description",
            "price",
            "active",
            "category",
            "categories_id",
        ]

    def create(self, validated_data):
        category_data = validated_data.pop("categories_id")
        product = Product.objects.create(**validated_data)
        product.category.set(category_data)
        return product

    def update(self, instance, validated_data):
        category_data = validated_data.pop("categories_id", None)
        instance = super().update(instance, validated_data)
        if category_data:
            instance.category.set(category_data)
        return instance
