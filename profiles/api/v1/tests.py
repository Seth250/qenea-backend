from rest_framework import status
from rest_framework.reverse import reverse as api_reverse
from rest_framework.test import APIClient, APITestCase

from profiles.models import Profile


class ProfilesAPITestCase(APITestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.test_password = 'Password@001'

        self.test_first_auth_data = {
            'email': 'eren.yaeger@test.com',
            'password': self.test_password
        }
        self.test_first_create_user_data = {
            'first_name': 'eren',
            'last_name': 'yaeger',
            'username': 'mr_freedom',
            **self.test_first_auth_data
        }

        self.test_second_auth_data = {
            'email': 'uzumaki.naruto@test.com',
            'password': self.test_password
        }
        self.test_second_create_user_data = {
            'first_name': 'naruto',
            'last_name': 'uzumaki',
            'username': 'kyubi_no_jinchuriki',
            **self.test_second_auth_data
        }

        self.signup_url = api_reverse('Accounts_API_v1:signup')
        self.login_url = api_reverse('Accounts_API_v1:login')
        self.user_profile_url = api_reverse('Profiles_API_v1:user-profile')

        # creating the first user and retriving the token
        self.client.post(path=self.signup_url, data=self.test_first_create_user_data)
        self.test_first_auth_token = self.client.post(
            path=self.login_url, data=self.test_first_auth_data
        ).data['auth_token']
        # creating the second user and retriving the token
        self.client.post(path=self.signup_url, data=self.test_second_create_user_data)
        self.test_second_auth_token = self.client.post(
            path=self.login_url, data=self.test_second_auth_data
        ).data['auth_token']

    def test_user_profile_retrieve(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.test_first_auth_token}') # passing auth token
        # testing profile retrieval
        test_response = self.client.get(path=self.user_profile_url)
        self.assertEqual(test_response.status_code, status.HTTP_200_OK)
        test_response_data = test_response.data
        self.assertEqual(test_response_data['user']['first_name'], self.test_first_create_user_data['first_name'])
        self.assertEqual(test_response_data['user']['last_name'], self.test_first_create_user_data['last_name'])
        self.assertEqual(test_response_data['user']['email'], self.test_first_create_user_data['email'])
        self.assertEqual(test_response_data['user']['username'], self.test_first_create_user_data['username'])
        test_profile = Profile.objects.get(id=test_response_data['id'])
        self.assertEqual(test_response_data['bio'], test_profile.bio)
        self.assertEqual(test_response_data['gender'], test_profile.gender)
        self.assertEqual(test_response_data['gender_choices'], test_profile.GENDER_CHOICES)
        self.assertEqual(test_response_data['followers_count'], test_profile.get_followers_count())
        self.assertEqual(test_response_data['following_count'], test_profile.get_following_count())
        self.assertEqual(test_response_data['date_of_birth'], test_profile.date_of_birth)

    def test_user_profile_update(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.test_first_auth_token}') # passing auth token
        # testing profile update
        test_profile_update_data = {
            'user': {
                'first_name': 'trevor',
                'last_name': 'belmont',
                'username': 'last_son_of_house_belmont'
            },
            'bio': 'This is a bio (no shit sherlock)',
            'gender': 'M'
        }
        test_response = self.client.put(path=self.user_profile_url, data=test_profile_update_data, format='json')
        self.assertEqual(test_response.status_code, status.HTTP_200_OK)
        test_response_data = test_response.data
        self.assertEqual(test_response_data['user']['first_name'], test_profile_update_data['user']['first_name'])
        self.assertEqual(test_response_data['user']['last_name'], test_profile_update_data['user']['last_name'])
        self.assertEqual(test_response_data['user']['username'], test_profile_update_data['user']['username'])
        self.assertEqual(test_response_data['bio'], test_profile_update_data['bio'])
        self.assertEqual(test_response_data['gender'], test_profile_update_data['gender'])


