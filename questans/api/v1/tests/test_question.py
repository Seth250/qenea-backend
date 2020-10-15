from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from questans.models import Question
from rest_framework.reverse import reverse as api_reverse
from django.contrib.auth import get_user_model


class QuestionAPITestCase(APITestCase):

	def setUp(self):
		self.client = APIClient()
		self.user_model = get_user_model()
		self.user_auth_token_url = api_reverse('Accounts-API:api_token_auth')
		self.question_list_create_url = api_reverse('Questions-API:question-list')
		# we're using different values for the email and username fields for test_user and test_superuser because
		# the values must be unique
		self.test_user_email = 'test-user@django.com'
		self.test_superuser_email = 'test-superuser@django.com'
		self.test_user_username = 'test-user'
		self.test_superuser_username = 'test-superuser'
		self.test_first_name = 'levi'
		self.test_last_name = 'ackerman'
		self.test_password = 'test_password001'

		self.test_create_user_data = {
			'email': self.test_user_email,
			'username': self.test_user_username,
			'first_name': self.test_first_name,
			'last_name': self.test_last_name,
			'password': self.test_password,
			'password2': self.test_password
		}

		self.test_create_superuser_data = {
			'email': self.test_superuser_email,
			'username': self.test_superuser_username,
			'password': self.test_password
		}

		self.test_title = "Test title"
		self.test_description = "Test description"

		self.test_question_data = {
			"title": self.test_title,
			"description": self.test_description
		}

		self.test_response_data = self.client.post(
			path=api_reverse('Accounts-API:user_signup'), 
			data=self.test_create_user_data
		).data

		self.test_user_token = self.client.post(
			path=self.user_auth_token_url,
			data={'username': self.test_response_data['email'], 'password': self.test_password}
		).data['token']

		self.test_superuser = self.user_model.objects.create_superuser(**self.test_create_superuser_data)

		self.test_superuser_token = self.client.post(
			path=self.user_auth_token_url,
			data={'username': self.test_superuser.email, 'password': self.test_password}
		).data['token']

	def test_question_list(self):
		# passing user token
		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.test_user_token}')
		# testing question list
		response = self.client.get(path=self.question_list_create_url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_question_list_with_unauthenticated_user(self):
		# testing question list
		response = self.client.get(path=self.question_list_create_url)
		# unauthenticated users are allowed GET requests on the question list endpoint i.e they can see all the
		# questions without being authenticated
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_create_question(self):
		# passing user token because only authenticated users can create questions
		self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.test_user_token}")
		# testing question creation
		response = self.client.post(path=self.question_list_create_url, data=self.test_question_data)
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)

	def test_create_question_with_unauthenticated_user(self):
		# testing question creation without passing user token
		response = self.client.post(path=self.question_list_create_url, data=self.test_question_data)
		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

	def test_question_detail(self):
		# passing user token
		self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.test_user_token}")
		# creating a question
		response = self.client.post(path=self.question_list_create_url, data=self.test_question_data)
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		# testing question detail
		question = Question.objects.get(title=self.test_title)
		# response = self.client.get(path=question.get_absolute_url())
		response = self.client.get(path=api_reverse('Questions-API:question-detail', kwargs={'pk': question.pk}))
		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


