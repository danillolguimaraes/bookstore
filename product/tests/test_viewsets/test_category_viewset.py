from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from product.models.category import Category

class TestCategoryViewSet(APITestCase):
    def setUp(self):
        # Criação do usuário e token de autenticação
        self.user = User.objects.create_user(username="danilloneo", password="Kamigawa3001%")
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        # Criação de uma categoria para o teste
        self.category = Category.objects.create(
            title="Tech", 
            slug="tech", 
            description="Technology related items", 
            active=True
        )

    def test_create_category(self):
        data = {
            "title": "Science",
            "slug": "science",
            "description": "Science related items",
            "active": True
        }

        response = self.client.post(
            reverse("category-list", kwargs={"version": "v1"}), 
            data, 
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "Science")

    def test_get_all_category(self):
        response = self.client.get(
            reverse("category-list", kwargs={"version": "v1"})
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["title"], self.category.title)
