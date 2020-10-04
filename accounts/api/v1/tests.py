from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model


class AccountsTestCase(APITestCase):

    def setUp(self):
        self.user_model = get_user_model()
        self.client = APIClient()
        self.test_email = 'test-email@django.com'
        self.test_username = 'test-user'
        self.test_first_name = 'eren'
        self.test_last_name = 'yeager'
        self.test_password = 'test_password' 

        self.test_user_data = {
            'email': self.test_email,
            'username': self.test_username,
            'first_name': self.test_first_name,
            'last_name': self.test_last_name,
            'password': self.test_password,
            'password2': self.test_password
        }

    def test_create_user(self):
        url = '/test/'
        response = self.client.post(url, data=self.test_user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
