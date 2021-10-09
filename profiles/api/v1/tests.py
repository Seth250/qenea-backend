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
        test_profile = Profile.objects.get(id=test_response_data['id'])
        self.assertEqual(test_profile.user.first_name, self.test_first_create_user_data['first_name'])
        self.assertEqual(test_profile.user.first_name, test_response_data['user']['first_name'])
        self.assertEqual(test_profile.user.last_name, self.test_first_create_user_data['last_name'])
        self.assertEqual(test_profile.user.last_name, test_response_data['user']['last_name'])
        self.assertEqual(test_profile.user.email, self.test_first_create_user_data['email'])
        self.assertEqual(test_profile.user.email, test_response_data['user']['email'])
        self.assertEqual(test_profile.user.username, self.test_first_create_user_data['username'])
        self.assertEqual(test_profile.user.username, test_response_data['user']['username'])
        self.assertEqual(test_profile.bio, test_response_data['bio'])
        self.assertEqual(test_profile.gender, test_response_data['gender'])
        self.assertEqual(test_profile.GENDER_CHOICES, test_response_data['gender_choices'])
        self.assertEqual(test_profile.get_followers_count(), test_response_data['followers_count'])
        self.assertEqual(test_profile.get_following_count(), test_response_data['following_count'])
        self.assertEqual(test_profile.date_of_birth, test_response_data['date_of_birth'])

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
            'gender': 'M',
            'date_of_birth': '2002-02-02'
        }
        test_response = self.client.put(path=self.user_profile_url, data=test_profile_update_data, format='json')
        self.assertEqual(test_response.status_code, status.HTTP_200_OK)
        test_response_data = test_response.data
        test_profile = Profile.objects.get(id=test_response_data['id'])
        self.assertEqual(test_profile.user.first_name, test_profile_update_data['user']['first_name'])
        self.assertEqual(test_profile.user.first_name, test_response_data['user']['first_name'])
        self.assertEqual(test_profile.user.last_name, test_profile_update_data['user']['last_name'])
        self.assertEqual(test_profile.user.last_name, test_response_data['user']['last_name'])
        self.assertEqual(test_profile.user.username, test_profile_update_data['user']['username'])
        self.assertEqual(test_profile.user.username, test_response_data['user']['username'])
        self.assertEqual(test_profile.bio, test_profile_update_data['bio'])
        self.assertEqual(test_profile.bio, test_response_data['bio'])
        self.assertEqual(test_profile.gender, test_profile_update_data['gender'])
        self.assertEqual(test_profile.gender, test_response_data['gender'])
        self.assertEqual(str(test_profile.date_of_birth), test_profile_update_data['date_of_birth'])
        self.assertEqual(str(test_profile.date_of_birth), test_response_data['date_of_birth'])
        # making sure the email hasn't changed
        self.assertEqual(test_profile.user.email, test_response_data['user']['email'])

    def test_profile_detail(self):
        test_first_profile_detail_url = api_reverse(
            'Profiles_API_v1:profile-detail',
            kwargs={'username': self.test_first_create_user_data['username']}
        )
        test_response = self.client.get(path=test_first_profile_detail_url)
        test_response_data = test_response.data
        test_profile = Profile.objects.get(id=test_response_data['id'])
        self.assertEqual(test_response.status_code, status.HTTP_200_OK)
        self.assertEqual(test_profile.user.first_name, self.test_first_create_user_data['first_name'])
        self.assertEqual(test_profile.user.first_name, test_response_data['user']['first_name'])
        self.assertEqual(test_profile.user.last_name, self.test_first_create_user_data['last_name'])
        self.assertEqual(test_profile.user.last_name, test_response_data['user']['last_name'])
        self.assertEqual(test_profile.user.email, self.test_first_create_user_data['email'])
        self.assertEqual(test_profile.user.email, test_response_data['user']['email'])
        self.assertEqual(test_profile.user.username, self.test_first_create_user_data['username'])
        self.assertEqual(test_profile.user.username, test_response_data['user']['username'])
        self.assertEqual(test_profile.bio, test_response_data['bio'])
        self.assertEqual(test_profile.gender, test_response_data['gender'])
        self.assertEqual(test_profile.get_followers_count(), test_response_data['followers_count'])
        self.assertEqual(test_profile.get_following_count(), test_response_data['following_count'])
        self.assertEqual(test_profile.date_of_birth, test_response_data['date_of_birth'])

