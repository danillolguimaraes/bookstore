import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from order.factories import OrderFactory, UserFactory
from product.factories import CategoryFactory, ProductFactory
from order.models import Order
from product.models import Product

class TestOrderViewSet(APITestCase):

    client = APIClient()

    def setUp(self):
        self.category = CategoryFactory(title="technology")
        self.product = ProductFactory(
            title="mouse", price=100
        )
        # Atribuindo a categoria ao produto
        self.product.category.add(self.category)
        self.order = OrderFactory(product=[self.product])

    def test_order(self):
        response = self.client.get(
            reverse("order-list", kwargs={"version": "v1"})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        order_data = json.loads(response.content)
        print(order_data)  # Verifique a estrutura dos dados para depuração

        # Acessar corretamente a lista de dados
        self.assertIsInstance(order_data, list)
        self.assertIsInstance(order_data[0]["product"], list)

        # Verificar o título do primeiro produto na lista
        self.assertEqual(
            order_data[0]["product"][0]["title"], self.product.title
        )
        self.assertEqual(
            order_data[0]["product"][0]["price"], self.product.price
        )
        self.assertEqual(
            order_data[0]["product"][0]["active"], self.product.active
        )
        self.assertEqual(
            order_data[0]["product"][0]["category"][0]["title"],
            self.category.title,
        )

    def test_create_order(self):
        user = UserFactory()
        product = ProductFactory()
        data = json.dumps({"products_id": [product.id], "user": user.id})

        response = self.client.post(
            reverse("order-list", kwargs={"version": "v1"}),
            data=data,
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        created_order = Order.objects.get(user=user)
        # Verifique se o pedido foi criado corretamente
        self.assertEqual(created_order.product.first().title, product.title)
