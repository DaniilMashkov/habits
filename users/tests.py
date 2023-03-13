from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User


class UserTestCase(APITestCase):
    def setUp(self):
        self.user = User(telegram_id='DaniilMashkov', is_staff=True)
        self.user.set_password('Aa111111')
        self.user.save()

        response = self.client.post('/api/token/', {'telegram_id': 'DaniilMashkov', 'password': 'Aa111111'})
        self.access_token = response.json().get('access')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        self.test_data = {'telegram_id': 'DaniilMashkov', "password": "Aa111111"}
        self.test_response_data = {'telegram_id': 'DaniilMashkov', "avatar": None, 'first_name': '', 'last_name': ''}

    def test_create_user(self):
        response = self.client.post('/users/create/', {'telegram_id': 'Mashkov', "password": "Aa111111"})

        self.assertEqual(response.json(), ['To continue start a chat with bot https://t.me/Suuupsupbot'])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_list_users(self):
        response = self.client.get('/users/')

        self.assertEqual(response.json(), [self.test_response_data])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_user(self):
        response = self.client.get('/users/1/')

        self.assertEqual(response.json(), self.test_response_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_destroy_user(self):
        response = self.client.delete('/users/delete/1/')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_update_user(self):
        response = self.client.patch('/users/1/', {"first_name": "Daniil"})

        self.assertEqual(response.json(), {
            'telegram_id': 'DaniilMashkov',
            'avatar': None,
            'first_name': 'Daniil',
            'last_name': ''
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
