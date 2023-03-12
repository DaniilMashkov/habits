from datetime import datetime
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User


class HabitTestCase(APITestCase):

    def setUp(self) -> None:
        self.user = User(telegram_id='admin', is_staff=True)
        self.user.set_password('Aa111111')
        self.user.save()

        response = self.client.post('/api/token/', {'telegram_id': 'admin', 'password': 'Aa111111'})
        self.access_token = response.json().get('access')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        self.json_current_time = datetime.now().strftime('%H:%M:%S')

        self.habit_test_data = {
            "time_to_do": self.json_current_time,
            "action": "to drink",
            "place_to_do": "anywhere",
            "reward": "good feeling",
            "is_related": False,
            "is_private": False,
            "periodicity": 7,
            "time_for_execute": 30
        }
        self.related_habit_test_data = {
            "time_to_do": self.json_current_time,
            "action": "to piss",
            "place_to_do": "bushes",
            "is_related": True,
            "is_private": False,
            "periodicity": 1,
            "time_for_execute": 60
        }

        self.response_test_habit_data = {
            "id": 1,
            "time_to_do": self.json_current_time,
            "action": "to drink",
            "place_to_do": "anywhere",
            "reward": "good feeling",
            "is_related": False,
            "related_habit": None,
            "is_private": False,
            "periodicity": 7,
            "time_for_execute": 30
        }

    def test_create_habit(self):
        response = self.client.post('/habits/', self.habit_test_data)

        self.assertEqual(response.json(), self.response_test_habit_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_list_habits(self):
        self.client.post('/habits/', self.habit_test_data)
        response = self.client.get('/habits/')

        self.assertEqual(response.json(), [self.response_test_habit_data, ])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_habit(self):
        self.client.post('/habits/', self.habit_test_data)
        response = self.client.get('/habits/1/')

        self.assertEqual(response.json(), self.response_test_habit_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_habit(self):
        self.client.post('/habits/', self.habit_test_data)
        response = self.client.delete('/habits/1/')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_update_habit(self):
        self.test_create_habit()
        self.client.post('/habits/', self.related_habit_test_data)
        response = self.client.patch('/habits/1/', {'related_habit': 2})

        self.assertEqual(
            response.json(), {
                "id": 1,
                "time_to_do": self.json_current_time,
                "action": "to drink",
                "place_to_do": "anywhere",
                "reward": "good feeling",
                "is_related": False,
                "related_habit": 2,
                "is_private": False,
                "periodicity": 7,
                "time_for_execute": 30
            })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
