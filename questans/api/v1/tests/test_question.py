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

		self.test_user_response_data = self.client.post(
			path=api_reverse('Accounts-API:user_signup'), 
			data=self.test_create_user_data
		).data

		self.test_user_token = self.client.post(
			path=self.user_auth_token_url,
			data={'username': self.test_user_response_data['email'], 'password': self.test_password}
		).data['token']

		self.test_superuser = self.user_model.objects.create_superuser(**self.test_create_superuser_data)

		self.test_superuser_token = self.client.post(
			path=self.user_auth_token_url,
			data={'username': self.test_superuser.email, 'password': self.test_password}
		).data['token']
		
		self.test_title = "Test title"
		self.test_description = "Test description"

		self.test_question_data = {
			"title": self.test_title,
			"description": self.test_description
		}

		self.test_question = Question.objects.create(**self.test_question_data, user=self.test_superuser)
		self.test_question_detail_url = api_reverse('Questions-API:question-detail', kwargs={'pk': self.test_question.pk})

	def test_question_list(self):
		# passing user token
		self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.test_user_token}')
		# testing question list
		response = self.client.get(path=self.question_list_create_url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_question_list_with_unauthenticated_user(self):
		# testing question list
		response = self.client.get(path=self.question_list_create_url)
		# unauthenticated users are allowed GET requests on the question list endpoint i.e they can view all the
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

	def test_create_question_with_invalid_title(self):
		# passing user token
		self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.test_user_token}")
		# testing question creation with empty title 
		self.test_question_data['title'] = ''
		response = self.client.post(path=self.question_list_create_url, data=self.test_question_data)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

	def test_create_question_with_invalid_description(self):
		# passing user token
		self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.test_user_token}")
		# testing question creation with empty description 
		self.test_question_data['description'] = ''
		response = self.client.post(path=self.question_list_create_url, data=self.test_question_data)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

	def test_question_detail(self):
		# passing user token
		self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.test_user_token}")
		# testing question detail for the question that we created in setUp
		response = self.client.get(path=self.test_question_detail_url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		# creating a question
		response = self.client.post(path=self.question_list_create_url, data=self.test_question_data)
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		# testing question detail
		question_detail_uri = response.data['uri']
		response = self.client.get(path=question_detail_uri)
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_question_detail_with_unauthenticated_user(self):
		# testing question detail for the question we created in setUp
		response = self.client.get(path=self.test_question_detail_url)
		# unauthenticated users are allowed GET requests on the question detail endpoint i.e they can view a
		# particular question without being authenticated
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_question_update(self):
		# passing user token
		self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.test_user_token}")
		# creating a question
		response = self.client.post(path=self.question_list_create_url, data=self.test_question_data)
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		question_detail_uri = response.data['uri']
		# changing question title
		self.test_question_data['title'] = 'Updated title'
		# testing question update
		response = self.client.put(path=question_detail_uri, data=self.test_question_data)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		# changing question description
		self.test_question_data['description'] = 'An Updated description'
		response = self.client.put(path=question_detail_uri, data=self.test_question_data)
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_question_update_with_prohibited_user(self):
		# passing user token
		self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.test_user_token}")
		 # changing question title
		self.test_question_data['title'] = 'An Updated Question Title'
		# testing question update for the question that we created in setUp
		response = self.client.put(path=self.test_question_detail_url, data=self.test_question_data)
		# an error would occur because only the object owner or superusers are allowed to update questions
		self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
		# changing question description
		self.test_question_data['description'] = 'An Updated Question Description'
		response = self.client.put(path=self.test_question_detail_url, data=self.test_question_data)
		self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

	def test_question_update_with_superuser(self):
		# passing user token
		self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.test_user_token}")
		# creating a question
		response = self.client.post(path=self.question_list_create_url, data=self.test_question_data)
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		question_detail_uri = response.data['uri']
		# changing the token to the superuser's token so that we can authenticate as the superuser
		self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.test_superuser_token}")
		# changing question title
		self.test_question_data['title'] = 'Do you hate me?'
		# testing question update
		response = self.client.put(path=question_detail_uri, data=self.test_question_data)
		# superusers are allowed to update questions even if they are not the owners
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		# changing question description
		self.test_question_data['description'] = 'My Pain is far greater than Yours!'
		response = self.client.put(path=question_detail_uri, data=self.test_question_data)
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_question_update_with_invalid_title(self):
		# passing user token
		self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.test_user_token}")
		# creating a question
		response = self.client.post(path=self.question_list_create_url, data=self.test_question_data)
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		question_detail_uri = response.data['uri']
		# testing question update with empty title
		self.test_question_data['title'] = ''
		response = self.client.put(path=question_detail_uri, data=self.test_question_data)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		# removing title from question data
		self.test_question_data.pop('title')
		# testing question update with no title field
		response = self.client.put(path=question_detail_uri, data=self.test_question_data)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


