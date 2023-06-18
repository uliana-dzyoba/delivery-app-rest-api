from django.contrib.auth import get_user_model
from django.urls import reverse
from model_bakery import baker
from rest_framework import status
from rest_framework.settings import api_settings
from rest_framework.test import APITestCase, force_authenticate, APIRequestFactory

from deliveryproject.test_utils import paginate_objects
from orders.mixins import parameter_to_date
from orders.models import MenuItem, Order
from orders.serializers import MenuItemSerializer, OrderSerializer, OrderCustomerSerializer


# Create your tests here.
class TestMenuItemDetailUpdateDeleteView(APITestCase):
    def setUp(self):
        self.menu_item = baker.make(MenuItem)
        self.url = reverse('menu_item', kwargs={'pk': self.menu_item.pk})
        self.admin = get_user_model().objects.create_superuser('admin@mail.com', 'admin', 'admin1234567890')

    def test_get_menu_item(self):
        response = self.client.get(self.url)
        menu_item = MenuItem.objects.get(pk=self.menu_item.pk)
        serializer = MenuItemSerializer(menu_item)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_menu_item(self):
        menu_item = baker.make(MenuItem)
        serializer = MenuItemSerializer(menu_item)
        serialized_data = serializer.data
        serialized_data['id'] = self.menu_item.id
        MenuItem.objects.get(pk=menu_item.pk).delete()
        self.client.force_authenticate(user=self.admin)
        response = self.client.put(self.url, serialized_data)
        self.assertEqual(response.data, serialized_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_menu_item(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class TestMenuItemPublicListCreateView(APITestCase):
    def setUp(self):
        self.url = reverse('menu')
        self.admin = get_user_model().objects.create_superuser('admin@mail.com', 'admin', 'admin1234567890')

    def test_list_menu_items(self):
        baker.make(MenuItem, _quantity=3)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_menu_item(self):
        menu_item = baker.make(MenuItem)
        serializer = MenuItemSerializer(menu_item)
        MenuItem.objects.get(pk=menu_item.pk).delete()
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(self.url, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(MenuItem.objects.count(), 1)


class TestOrderDetailUpdateDeleteView(APITestCase):
    def setUp(self):
        self.order = baker.make(Order)
        self.url = reverse('order', kwargs={'pk': self.order.pk})
        self.user = baker.make(get_user_model())
        self.admin = get_user_model().objects.create_superuser('admin@mail.com', 'admin', 'admin1234567890')

    def test_get_order(self):
        self.client.force_authenticate(user=self.order.customer)
        response = self.client.get(self.url)
        order = Order.objects.get(pk=self.order.pk)
        serializer = OrderCustomerSerializer(order)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_order(self):
        order = baker.make(Order)
        order.customer = self.order.customer
        order.save(update_fields=['customer'])
        serializer = OrderCustomerSerializer(order)
        serialized_data = serializer.data
        serialized_data['id'] = self.order.id
        Order.objects.get(pk=order.pk).delete()
        self.client.force_authenticate(user=self.admin)
        response = self.client.put(self.url, serialized_data)
        self.assertEqual(response.data, serialized_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_order(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class TestOrderListCreateView(APITestCase):
    def setUp(self):
        self.url = reverse('orders')
        self.user = baker.make(get_user_model())
        self.admin = get_user_model().objects.create_superuser('admin@mail.com', 'admin', 'admin1234567890')
        self.factory = APIRequestFactory()
        pagination_class = api_settings.DEFAULT_PAGINATION_CLASS
        self.paginator = pagination_class()

    def test_list_orders_admin(self):
        baker.make(Order, _quantity=3)
        orders = Order.objects.all().order_by('-delivery_at')
        request = self.factory.get(self.url)
        force_authenticate(request, user=self.admin)
        request.query_params = {'page': 0}
        url = self.url
        page_num = 1
        while True:
            request.query_params['page'] = page_num
            paginated = paginate_objects(request, self.paginator, orders, OrderCustomerSerializer)
            self.client.force_authenticate(user=self.admin)
            response = self.client.get(url)
            self.assertEqual(response.data, paginated.data)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            url = response.data.get('next')
            if not url:
                break
            page_num += 1

    def test_list_orders_customer(self):
        all_orders = baker.make(Order, _quantity=3)
        all_orders[0].customer = self.user
        orders = Order.objects.filter(customer=self.user).order_by('-delivery_at')
        request = self.factory.get(self.url)
        force_authenticate(request, user=self.user)
        request.query_params = {'page': 0}
        url = self.url
        page_num = 1
        while True:
            request.query_params['page'] = page_num
            paginated = paginate_objects(request, self.paginator, orders, OrderCustomerSerializer)
            self.client.force_authenticate(user=self.user)
            response = self.client.get(url)
            self.assertEqual(response.data, paginated.data)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            url = response.data.get('next')
            if not url:
                break
            page_num += 1

    # def test_create_menu_item(self):
    #     menu_item = baker.make(Order)
    #     serializer = OrderSerializer(menu_item)
    #     Order.objects.get(pk=menu_item.pk).delete()
    #     self.client.force_authenticate(user=self.admin)
    #     response = self.client.post(self.url, serializer.data)
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(Order.objects.count(), 1)


class TestOrderStatusDateFilterMixin(APITestCase):
    pass
