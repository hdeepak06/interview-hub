from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from apps.assessments.models import TestAttempt

class DashboardTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='dash_tester', password='Password123!')
        self.client.force_authenticate(user=self.user)

    def test_new_user_dashboard_returns_zeroed_stats_without_fakes(self):
        # A new user has 0 attempts; verify no hardcoded or fake statistics
        response = self.client.get('/api/dashboard/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'success')
        self.assertEqual(response.data['questions_attempted'], 0)
        self.assertEqual(response.data['questions_correct'], 0)
        self.assertEqual(response.data['accuracy_percentage'], 0.0)
        self.assertEqual(response.data['mock_tests_completed'], 0)
        self.assertEqual(len(response.data['recent_activities']), 0)

    def test_dashboard_aggregates_real_test_attempts(self):
        TestAttempt.objects.create(
            student=self.user,
            subject_slug='python',
            total_questions=10,
            correct_answers=8,
            score_percentage=80.0,
            is_completed=True
        )

        response = self.client.get('/api/dashboard/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['questions_attempted'], 10)
        self.assertEqual(response.data['questions_correct'], 8)
        self.assertEqual(response.data['accuracy_percentage'], 80.0)
        self.assertEqual(response.data['mock_tests_completed'], 1)

