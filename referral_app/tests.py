from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import UserModel, Referral
from rest_framework.authtoken.models import Token


class UserRegistrationTestCase(APITestCase):
    def test_user_registration(self):
        url = reverse('register')
        data = {
            'name': 'Jay Chhaniyara',
            'email': 'jaython.dev@gmail.com',
            'password': '1234',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class UserLoginTestCase(APITestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(
            name='Joy', email='jo@admin.com', password='test')

    def test_user_login(self):
        url = reverse('user-login')
        data = {
            'email': 'jo@admin.com',
            'password': 'test'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertIn('user_id', response.data)


class UserDetailsTestCase(APITestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(
            name='Jay', email='john@example.com', password='testpassword')

    def test_user_details(self):
        url = reverse('user-details')
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user']['id'], self.user.id)


class UserReferralTestCase(APITestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(
            name='John Doe', email='john@example.com', password='testpassword')
        self.referral = Referral.objects.create(
            user=self.user, referred_by=self.user)

    def test_user_referrals(self):
        url = reverse('referrals')
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Use results for paginated response
        self.assertEqual(len(response.data['results']), 1)


class AuthenticatedUserTestCase(APITestCase):
    def test_unauthenticated_user_access(self):
        url = reverse('user-details')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        url = reverse('referrals')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
