import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

from order.factories import OrderFactory, UserFactory
from product.factories import CategoryFactory, ProductFactory
from order.models import Order


class TestOrderViewSet(APITestCase):

    def setUp(self):
        # Criação do usuário e token de autenticação
        self.user = User.objects.create_user(
            username="danilloneo", password="Kamigawa3001%"
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

        # Criação de categoria, produto e pedido para os testes
        self.category = CategoryFactory(title="technology")
        self.product = ProductFactory(title="mouse", price=100)
        self.product.category.add(self.category)
        self.order = OrderFactory(product=[self.product], user=self.user)

    def test_order(self):
        response = self.client.get(reverse("order-list", kwargs={"version": "v1"}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        order_data = response.json()

        # Verifique se os dados estão em uma lista na chave "results" devido à paginação
        self.assertIsInstance(order_data["results"], list)
        self.assertIsInstance(order_data["results"][0]["product"], list)

        # Verificar o título do primeiro produto na lista
        self.assertEqual(
            order_data["results"][0]["product"][0]["title"], self.product.title
        )
        self.assertEqual(
            order_data["results"][0]["product"][0]["price"], self.product.price
        )
        self.assertEqual(
            order_data["results"][0]["product"][0]["active"], self.product.active
        )
        self.assertEqual(
            order_data["results"][0]["product"][0]["category"][0]["title"],
            self.category.title,
        )

    def test_create_order(self):
        # Criação de um novo usuário e produto
        user = UserFactory()
        product = ProductFactory()
        data = {"products_id": [product.id], "user": user.id}

        response = self.client.post(
            reverse("order-list", kwargs={"version": "v1"}),
            data=json.dumps(data),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        created_order = Order.objects.get(user=user)
        # Verifique se o pedido foi criado corretamente
        self.assertEqual(created_order.product.first().title, product.title)
