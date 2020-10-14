from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from questans.models import Question
from rest_framework.reverse import reverse as api_reverse
from django.contrib.auth import get_user_model


class QuestionAPITestCase(APITestCase):

	def setUp(self):
		self.client = APIClient()
		self.user_model = get_user_model()
        self.test_create_user_data = {
            'email': 'test-user@django.com',
            'username': 'test-user',
            'first_name': 'levi',
            'last_name': 'ackerman',
            'password': 'test_password001',
            'password2': 'test_password001'
        }
		self.test_question_data = {
			"title": "Test Title",
			"description": "Test Description"
		}
		self.test_user = self.client.post(path=api_reverse('Accounts-API:user_signup'), data=self.test_user_data)

	def test_create_question(self):
		response = self.client.post(path=self.list_create_url, data=self.test_question_data)
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)


