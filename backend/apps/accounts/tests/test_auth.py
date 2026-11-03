from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from apps.accounts.models import StudentProfile

class AccountsAuthTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = '/api/auth/register/'
        self.login_url = '/api/auth/login/'
        self.profile_url = '/api/auth/profile/'

    def test_student_registration_success(self):
        payload = {
            'username': 'rahul_cse',
            'email': 'rahul@example.com',
            'first_name': 'Rahul',
            'last_name': 'Sharma',
            'password': 'SecurePassword123!',
            'branch': 'CSE',
            'college_name': 'VTU Institute of Technology'
        }
        response = self.client.post(self.register_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('token', response.data)
        self.assertEqual(response.data['user']['username'], 'rahul_cse')

        # Verify profile creation in database
        profile = StudentProfile.objects.get(user__username='rahul_cse')
        self.assertEqual(profile.branch, 'CSE')
        self.assertEqual(profile.college_name, 'VTU Institute of Technology')

    def test_registration_duplicate_username_fails(self):
        User.objects.create_user(username='existing_user', email='first@example.com', password='Password123!')
        payload = {
            'username': 'existing_user',
            'email': 'second@example.com',
            'first_name': 'Test',
            'password': 'Password123!',
            'branch': 'ISE'
        }
        response = self.client.post(self.register_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data['errors'])

    def test_login_success(self):
        User.objects.create_user(username='deepak_dev', email='deepak@example.com', password='MyStrongPassword123')
        payload = {
            'username': 'deepak_dev',
            'password': 'MyStrongPassword123'
        }
        response = self.client.post(self.login_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_login_invalid_password_fails(self):
        User.objects.create_user(username='deepak_dev', password='MyStrongPassword123')
        payload = {
            'username': 'deepak_dev',
            'password': 'WrongPassword!'
        }
        response = self.client.post(self.login_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

