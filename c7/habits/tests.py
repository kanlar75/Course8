from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from habits.models import Habit
from users.models import User


class HabitTestCase(APITestCase):
    APITestCase.maxDiff = None

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

        self.habit = Habit.objects.create(
            place='test_place',
            time='10:30:00',
            action='test_action',
            estimated_time=120,
            is_public=True,
            user=self.user

        )
        self.client.force_authenticate(user=self.user)

    def test_habit_list(self):
        """Тест получения списка привычек """

        response = self.client.get(
            reverse('habits:habit_list')
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {
                "count": 1,
                "next": None,
                "previous": None,
                "results": [
                    {'id': 6,
                     'user': 5,
                     'place': 'test_place',
                     'time': '10:30:00',
                     'action': 'test_action',
                     'connected_habit': None,
                     'periodicity': 1,
                     'reward': None,
                     'estimated_time': 120,
                     'is_pleasant': False,
                     'last_reminder': None,
                     'is_public': True}
                ]
            }
        )

    def test_habit_create(self):
        """Тест создания привычки """

        self.client.force_authenticate(user=self.user)

        data = {
            'place': 'test_place_create',
            'time': '12:30',
            'action': 'test_action_create',
            'estimated_time': 100,
            'periodicity': 3

        }

        response = self.client.post(
            reverse('habits:habit_create'),
            data=data
        )
        self.habit.refresh_from_db()

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(Habit.objects.all().count(), 2)
        self.assertTrue(
            Habit.objects.filter(action='test_action_create').exists())

    def test_habit_bad_create(self):
        """Тест создания привычки с плохой периодичностью """

        self.client.force_authenticate(user=self.user)

        data_bad = {
            'place': 'test_place_bad_create',
            'time': '12:30',
            'action': 'test_action_bad_create',
            'estimated_time': 100,
            'periodicity': 8

        }

        response = self.client.post(
            reverse('habits:habit_create'),
            data=data_bad
        )
        self.habit.refresh_from_db()

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertEqual(Habit.objects.all().count(), 1)
        self.assertFalse(
            Habit.objects.filter(action='test_action_bad_create').exists())

    def test_habit_update(self):
        """ Тест обновления привычки """

        data = {
            'place': 'test_place_update',
        }

        response = self.client.patch(
            reverse('habits:habit_update', args=[self.habit.pk]),
            data=data)
        self.habit.refresh_from_db()

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            self.habit.place,
            'test_place_update'
        )

    def test_habit_destroy(self):
        """Тест удаления привычки """

        self.client.delete(
            reverse('habits:habit_delete', args=[self.habit.pk])
        )

        self.assertFalse(Habit.objects.filter(id=self.habit.pk).exists())

    def test_get_list_public(self):
        """ Тест получения списка публичных привычек """

        response = self.client.get(
            reverse('habits:public_habit_list')
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {
                "count": 1,
                "next": None,
                "previous": None,
                "results": [
                    {
                        'action': 'test_action',
                        'connected_habit': None,
                        'estimated_time': 120,
                        'id': 1,
                        'is_pleasant': False,
                        'is_public': True,
                        'last_reminder': None,
                        'periodicity': 1,
                        'place': 'test_place',
                        'reward': None,
                        'time': '10:30:00',
                        'user': 1
                    }
                ]
            }
        )
