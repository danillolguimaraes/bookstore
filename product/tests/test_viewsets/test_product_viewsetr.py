from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from product.models.product import Product, Category
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User


class TestProductViewSet(APITestCase):
    def setUp(self):
        # Criação do usuário e token de autenticação
        self.user = User.objects.create_user(username="danilloneo", password="Kamigawa3001%")
        self.token = Token.objects.create(user=self.user)

        # Criação da categoria e do produto para os testes
        self.category = Category.objects.create(
            title="Tech", 
            slug="tech", 
            description="Technology related items", 
            active=True
        )

        self.product = Product.objects.create(
            title="Mouse",
            description="Wireless mouse",
            price=100,
            active=True
        )
        self.product.category.add(self.category)

        # Definindo o token de autenticação nos cabeçalhos de todas as requisições
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_create_product(self):
        # Dados para criar um novo produto
        data = {
            "title": "Keyboard",
            "description": "Mechanical keyboard",
            "price": 150,
            "active": True,
            "categories_id": [self.category.id]
        }

        response = self.client.post(
            reverse("product-list", kwargs={"version": "v1"}), 
            data, 
            format="json"
        )

        # Verificações dos resultados esperados
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "Keyboard")
        self.assertEqual(response.data["category"][0]["title"], "Tech")

    def test_get_all_product(self):
        response = self.client.get(
            reverse("product-list", kwargs={"version": "v1"})
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"][0]["title"], self.product.title)
