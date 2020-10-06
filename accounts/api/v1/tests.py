from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.reverse import reverse as api_reverse


class AccountsTestCase(APITestCase):

    def setUp(self):
        self.user_model = get_user_model()
        self.client = APIClient()
        self.test_email = 'test-email@django.com'
        self.test_username = 'test-user'
        self.test_first_name = 'eren'
        self.test_last_name = 'yeager'
        self.test_password = 'test_password001' 
        self.create_url = api_reverse('Accounts-API:user_signup')
        self.auth_token_url = api_reverse('Accounts-API:api_token_auth')
        self.user_list_url = api_reverse('Accounts-API:user-list')

        self.test_create_data = {
            'email': self.test_email,
            'username': self.test_username,
            'first_name': self.test_first_name,
            'last_name': self.test_last_name,
            'password': self.test_password,
            'password2': self.test_password
        }

        self.test_auth_data = {
            # because of our custom user model, username field takes an email
            'username': self.test_email,
            'password': self.test_password
        }

    def test_create_superuser(self):
        self.user_model.objects.create_superuser(
            email=self.test_email, username=self.test_username, password=self.test_password
        )
        super_user = self.user_model.objects.get(email=self.test_email)
        self.assertEqual(super_user.email, self.test_email)
        self.assertEqual(super_user.username, self.test_username)
        self.assertTrue(super_user.is_staff)
        self.assertTrue(super_user.is_superuser)

    def test_create_user(self):
        response = self.client.post(path=self.create_url, data=self.test_create_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        test_user = self.user_model.objects.get(email=self.test_email)
        self.assertEqual(test_user.email, self.test_email)
        self.assertEqual(test_user.username, self.test_username)
        self.assertEqual(test_user.first_name, self.test_first_name)
        self.assertEqual(test_user.last_name, self.test_last_name)
        self.assertFalse(test_user.is_staff)
        self.assertFalse(test_user.is_superuser)

    def test_create_user_with_invalid_email(self):
        self.test_create_data['email'] = 'test-email'
        response = self.client.post(path=self.create_url, data=self.test_create_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.test_create_data['email'] = 'test_email@django.c'
        response = self.client.post(path=self.create_url, data=self.test_create_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.test_create_data['email'] = ''
        response = self.client.post(path=self.create_url, data=self.test_create_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # max length for an EmailField is 254 characters, anything more than that should throw an error
        self.test_create_data['email'] = f'{"i" * 244}@django.com'
        response = self.client.post(path=self.create_url, data=self.test_create_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_with_invalid_username(self):
        self.test_create_data['username'] = ''
        response = self.client.post(path=self.create_url, data=self.test_create_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # max length for our username field is 25 characters, anything more than that should throw an error
        self.test_create_data['username'] = f'{"i" * 26}'
        response = self.client.post(path=self.create_url, data=self.test_create_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_with_invalid_firstname(self):
        self.test_create_data['first_name'] = ''
        response = self.client.post(path=self.create_url, data=self.test_create_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # max length for our first_name field is 25 characters, anything more than that should throw an error
        self.test_create_data['first_name'] = f'{"e" * 26}'
        response = self.client.post(path=self.create_url, data=self.test_create_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_with_invalid_lastname(self):
        self.test_create_data['last_name'] = ''
        response = self.client.post(path=self.create_url, data=self.test_create_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # max length for our last_name field is 25 characters, anything more than that should throw an error
        self.test_create_data['last_name'] = f'{"e" * 26}'
        response = self.client.post(path=self.create_url, data=self.test_create_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_with_invalid_passwords(self):
        # minimum length for password is 8 characters, anything less than that should throw an error
        self.test_create_data['password'] = self.test_create_data['password2'] = 'passwor'
        response = self.client.post(path=self.create_url, data=self.test_create_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # using a commmon password should throw an error
        self.test_create_data['password'] = self.test_create_data['password2'] = 'password'
        response = self.client.post(path=self.create_url, data=self.test_create_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # using an entirely numeric password should throw an error
        self.test_create_data['password'] = self.test_create_data['password2'] = '12345678'
        response = self.client.post(path=self.create_url, data=self.test_create_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # using a password with only letters should throw an error
        self.test_create_data['password'] = self.test_create_data['password2'] = 'sasageyo'
        response = self.client.post(path=self.create_url, data=self.test_create_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # using a password with less than three digits should throw an error
        self.test_create_data['password'] = self.test_create_data['password2'] = 'test_password00'
        response = self.client.post(path=self.create_url, data=self.test_create_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_with_mismatched_passwords(self):
        self.test_create_data['password2'] = 'sasageyo'
        response = self.client.post(path=self.create_url, data=self.test_create_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_with_existing_username(self):
        self.client.post(path=self.create_url, data=self.test_create_data)
        # replacing the email so it doesn't throw an error for the email field
        self.test_create_data['email'] = 'another-test-email@django.com'
        # using an already existing username should throw an error
        response = self.client.post(path=self.create_url, data=self.test_create_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_with_existing_email(self):
        self.client.post(path=self.create_url, data=self.test_create_data)
        # replacing the username so it doesn't throw an error for the username fied
        self.test_create_data['username'] = 'another-test-user'
        # using an already existing email should throw an error
        response = self.client.post(path=self.create_url, data=self.test_create_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_obtain_user_token(self):
        # creating a user so that we can get the token for that user
        response = self.client.post(path=self.create_url, data=self.test_create_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # testing user auth token acquisition
        response = self.client.post(path=self.auth_token_url, data=self.test_auth_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_obtain_user_token_with_incorrect_details(self):
        # creating a user
        response = self.client.post(path=self.create_url, data=self.test_create_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # testing user auth token acquisition with incorrect details
        self.test_auth_data['username'] = 'test-user'
        response = self.client.post(path=self.auth_token_url, data=self.test_auth_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_list(self):
        # creating a superuser
        self.user_model.objects.create_superuser(
            email=self.test_email, username=self.test_username, password=self.test_password
        )
        # user auth token acquisition
        response = self.client.post(path=self.auth_token_url, data=self.test_auth_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        auth_token = response.data['token']
        # passing user token
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {auth_token}")
        # testing user list
        response = self.client.get(path=self.user_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_list_with_no_auth_token(self):
        response = self.client.get(path=self.user_list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_list_with_normal_user(self):
        # creating a normal user
        response = self.client.post(path=self.create_url, data=self.test_create_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)        
        # user auth token acquisition
        response = self.client.post(path=self.auth_token_url, data=self.test_auth_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        auth_token = response.data['token']
        # passing user token
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {auth_token}")
        # testing user list
        response = self.client.get(path=self.user_list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
