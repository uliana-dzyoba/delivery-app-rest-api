from django.contrib.auth import get_user_model
from django.urls import reverse
from model_bakery import baker
from rest_framework import status
from rest_framework.settings import api_settings
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate

from authentication.serializers import UserSerializer, UserPublicSerializer
from deliveryproject.test_utils import paginate_objects


# Create your tests here.
class TestUserDetailDeleteView(APITestCase):
    def setUp(self):
        self.user = baker.make(get_user_model())
        self.url = reverse('user', kwargs={'pk': self.user.pk})
        self.admin = get_user_model().objects.create_superuser('admin@mail.com', 'admin', 'admin1234567890')

    def test_get_user(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(self.url)
        user = get_user_model().objects.get(pk=self.user.pk)
        serializer = UserSerializer(user)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_user_auto(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        user = get_user_model().objects.get(pk=self.user.pk)
        serializer = UserSerializer(user)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_user(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class TestUserListView(APITestCase):
    def setUp(self):
        self.url = reverse('users')
        self.users = baker.make(get_user_model(), _quantity=3)
        self.admin = get_user_model().objects.create_superuser('admin@mail.com', 'admin', 'admin1')
        self.client.force_authenticate(user=self.admin)
        self.factory = APIRequestFactory()
        pagination_class = api_settings.DEFAULT_PAGINATION_CLASS
        self.paginator = pagination_class()

    def test_list_users(self):
        users = get_user_model().objects.all().order_by('id')
        request = self.factory.get(self.url)
        force_authenticate(request, user=self.admin)
        request.query_params = {'page': 0}
        url = self.url
        page_num = 1
        while True:
            request.query_params['page'] = page_num
            paginated = paginate_objects(request, self.paginator, users, UserPublicSerializer)
            response = self.client.get(url)
            self.assertEqual(response.data, paginated.data)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            url = response.data.get('next')
            if not url:
                break
            page_num += 1


class TestUserSignUpView(APITestCase):
    def setUp(self):
        self.url = reverse('sign_up')

    def test_create_valid_user(self):
        data = {
            'username': 'user',
            'email': 'user@mail.com',
            'password': 'user1234567890'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(get_user_model().objects.count(), 1)

    def test_create_invalid_user(self):
        data = {
            'username': 'user',
            'email': 'user@mail.com',
            'password': ''
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
