from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from apps.content.models import Subject, Question
from apps.progress.models import Bookmark, StudentProgress

class ProgressTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='bookmark_tester', password='Password123!')
        self.client.force_authenticate(user=self.user)

        self.subject = Subject.objects.create(name='Python', slug='python')
        self.question = Question.objects.create(
            subject=self.subject,
            difficulty='easy',
            question_text='Sample question for bookmarking',
            correct_answer='Sample answer',
            explanation='Sample explanation',
            review_status='published'
        )

    def test_create_and_delete_bookmark(self):
        # Create bookmark
        response = self.client.post('/api/bookmarks/', {'question': self.question.id}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Bookmark.objects.filter(user=self.user).count(), 1)

        # Duplicate bookmark attempt should return existing without error
        response2 = self.client.post('/api/bookmarks/', {'question': self.question.id}, format='json')
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Bookmark.objects.filter(user=self.user).count(), 1)

        # List bookmarks
        list_resp = self.client.get('/api/bookmarks/')
        self.assertEqual(list_resp.status_code, status.HTTP_200_OK)
        results = list_resp.data['results'] if 'results' in list_resp.data else list_resp.data
        self.assertEqual(len(results), 1)

        # Delete bookmark
        bookmark_id = results[0]['id']
        del_resp = self.client.delete(f'/api/bookmarks/{bookmark_id}/')
        self.assertEqual(del_resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Bookmark.objects.filter(user=self.user).count(), 0)

