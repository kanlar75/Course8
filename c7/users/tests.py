import io
import sys

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from users.models import User


class UserTestCase(APITestCase):
    def setUp(self):
        """Заполнение первичных данных """

        self.user = User.objects.create(
            email='user@test.com',
            is_staff=False,
            is_superuser=False,
            is_active=True,
        )
        self.user.set_password('12345')
        self.user.save()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_user_create(self):
        """ Тест создания пользователя """

        data = {
            'email': 'user1@test.com',
            'password': '12345',
            'chat_id': '12345123'
        }

        response = self.client.post(
            reverse('users:user_create'),
            data=data
        )
        self.assertEqual(
            2,
            User.objects.all().count()
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_create_without_chat_id(self):
        """ Тест создания пользователя без chat_id """

        data = {
            'email': 'user1@test.com',
            'password': '12345'
        }
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput

        self.client.post(
            reverse('users:user_create'),
            data=data
        )

        sys.stdout = sys.__stdout__
        self.assertEqual(capturedOutput.getvalue(), 'chat_id нужен для '
                                                    'отправки уведомлений\n')

    def test_users_list(self):
        """ Тест получения списка пользователей """

        response = self.client.get(
            reverse('users:user_list')
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_retrieve(self):
        """Test детальной информации о пользователе """

        response = self.client.get(
            reverse('users:user_detail',
                    args=[self.user.pk])
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_update(self):
        """ Тест обновления пользователя """

        data = {
            'chat_id': '12345123',
        }
        response = self.client.patch(
            reverse('users:user_update',
                    args=[self.user.pk]),
            data=data
        )
        self.user.refresh_from_db()

        self.assertEqual(
            self.user.chat_id,
            '12345123'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_destroy(self):
        """ Тест удаления пользователя """

        response = self.client.delete(
            reverse('users:user_delete',
                    args=[self.user.pk]),
        )
        self.assertFalse(User.objects.filter(id=self.user.pk).exists())
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
