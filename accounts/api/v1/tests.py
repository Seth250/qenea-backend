from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework import test
from rest_framework.test import APITestCase, APIClient
from rest_framework.reverse import reverse as api_reverse


User = get_user_model()

class AccountsAPITestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.test_email = 'test-email@django.com'
        self.test_username = 'test_user'
        self.test_first_name = 'eren'
        self.test_last_name = 'yeagar'
        self.test_password = 'Password@001'

        self.test_auth_data = {
            'email': self.test_email,
            'password': self.test_password
        }

        self.test_create_user_data = {
            'first_name': self.test_first_name,
            'last_name': self.test_last_name,
            **self.test_auth_data,
        }

        self.test_user_signup_data = {
            'username': self.test_username,
            **self.test_create_user_data,
            'password2': self.test_password
        }

        self.signup_url = api_reverse('Accounts_API_v1:signup')
        self.login_url = api_reverse('Accounts_API_v1:login')
        self.logout_url = api_reverse('Accounts_API_v1:logout')

    def test_create_superuser(self):
        User.objects.create_superuser(**self.test_create_user_data)
        test_superuser = User.objects.get(email=self.test_create_user_data['email'])
        self.assertEqual(test_superuser.first_name, self.test_create_user_data['first_name'])
        self.assertEqual(test_superuser.last_name, self.test_create_user_data['last_name'])
        self.assertEqual(test_superuser.email, self.test_create_user_data['email'])
        self.assertTrue(test_superuser.is_staff)
        self.assertTrue(test_superuser.is_superuser)

    def test_user_signup(self):
        test_response = self.client.post(path=self.signup_url, data=self.test_user_signup_data)
        self.assertEqual(test_response.status_code, status.HTTP_201_CREATED)
        test_user = User.objects.get(email=self.test_user_signup_data['email'])
        self.assertEqual(test_user.first_name, self.test_user_signup_data['first_name'])
        self.assertEqual(test_user.last_name, self.test_user_signup_data['last_name'])
        self.assertEqual(test_user.email, self.test_user_signup_data['email'])
        self.assertFalse(test_user.is_staff)
        self.assertFalse(test_user.is_superuser)
        self.assertEqual(test_user.profile.username, self.test_user_signup_data['username'])

    def test_obtain_user_token(self):
        # before we can obtain the token, a user needs to be created
        test_res = self.client.post(path=self.signup_url, data=self.test_user_signup_data)
        self.assertEqual(test_res.status_code, status.HTTP_201_CREATED)
        # testing user auth token acquisition
        test_response = self.client.post(path=self.login_url, data=self.test_auth_data)
        self.assertEqual(test_response.status_code, status.HTTP_200_OK)
        test_auth_token = test_response.data['auth_token']
        test_user = User.objects.get(email=self.test_user_signup_data['email'])
        self.assertEqual(test_user.auth_token.key, test_auth_token)

    def test_user_token_logout(self):
        # to test token logout, a user needs to be created
        test_res = self.client.post(path=self.signup_url, data=self.test_user_signup_data)
        self.assertEqual(test_res.status_code, status.HTTP_201_CREATED)
        # the user also needs to be authenticated (token login) before logout can occur
        test_res = self.client.post(path=self.login_url, data=self.test_auth_data)
        self.assertEqual(test_res.status_code, status.HTTP_200_OK)
        test_auth_token = test_res.data['auth_token']
        # testing token logout
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {test_auth_token}') # passing the user's auth token
        test_response = self.client.post(path=self.logout_url)
        self.assertEqual(test_response.status_code, status.HTTP_204_NO_CONTENT)
