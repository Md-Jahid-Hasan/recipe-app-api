from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

CREATE_USER_URL = reverse('users:create')
CREATE_TOKEN = reverse('users:token')
ME_URL = reverse('users:me')


def create_user(**params):
    return get_user_model().objects.create_manager(**params)


class PublicUserAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_user(self):
        """Test creating user with valid user payload"""
        payload = {
            'email': 'rbbjahid@gmail.com',
            'password': 'testpass',
            'name': 'Test Name',
        }

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exist(self):
        """Its check User has already exists failed"""
        payload = {'email': "rbbjahid@gmail.com", 'password': 'testpass'}
        get_user_model().objects.create_manager(payload['email'], payload['password'])

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def password_too_short(self):
        payload = {'email': "rbbjahid@gmail.com", 'password': 'tp'}
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()

        self.assertFalse(user_exists)

    def create_token_for_user(self):
        """Test that a token is created for user"""
        payload = {"email": "test@gmail.com", 'password': "testpass"}
        create_user(**payload)
        res = self.client.post(CREATE_TOKEN, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_data(self):
        """Test that token is not create when invalid data enter"""
        payload = {"email": "test@gmail.com", 'password': "testpass"}
        create_user(**payload)
        res = self.client.post(CREATE_TOKEN, {"email": "test@gmail.com", "password": "wrong"})

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)

    def test_not_create_token_user_not_exists(self):
        """Test  that token is not create when user not exists"""
        payload = {"email": "test@gmail.com", 'password': "testpass"}
        res = self.client.post(CREATE_TOKEN, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """Test that not create token when missing any field"""
        res = self.client.post(CREATE_TOKEN, {"email": "test@gmail.com", "password": ""})
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_unauthorized_user(self):
        """Authentication is required for user"""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTest(TestCase):
    """Test Api request that require Authentication"""

    def setUp(self):
        self.user = create_user(
            email='rbbjahid@gmail.com',
            password='pass123',
            name='Name',
        )

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """Test retrieving profile for logged in user"""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'name': self.user.name,
            'email': self.user.email
        })

    def test_post_is_not_allowed(self):
        """Test post is not allowed"""
        res = self.client.post(ME_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_user_update_profile(self):
        """Test Updating the user profile for authenticate user"""
        payload = {'name': 'newname', 'password': 'pas12'}
        res = self.client.patch(ME_URL, payload)

        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)






