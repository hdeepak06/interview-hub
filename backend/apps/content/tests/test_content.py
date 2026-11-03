from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from apps.content.models import Subject, Topic, Question, AnswerOption

class ContentAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.python_subject = Subject.objects.create(
            name='Python', slug='python', target_questions=100
        )
        self.sql_subject = Subject.objects.create(
            name='SQL', slug='sql', target_questions=100
        )

        # Published question
        self.pub_question = Question.objects.create(
            subject=self.python_subject,
            difficulty='easy',
            question_text='What is the output of bool([]) in Python?',
            correct_answer='False',
            explanation='Empty collections in Python evaluate to False in a boolean context.',
            review_status='published',
            is_active=True
        )
        AnswerOption.objects.create(
            question=self.pub_question, option_label='A', option_text='True', is_correct=False
        )
        AnswerOption.objects.create(
            question=self.pub_question, option_label='B', option_text='False', is_correct=True
        )

        # Draft question (must NOT be visible in public API)
        self.draft_question = Question.objects.create(
            subject=self.python_subject,
            difficulty='medium',
            question_text='Draft unapproved question',
            correct_answer='Pending',
            explanation='Draft',
            review_status='draft',
            is_active=True
        )

    def test_list_subjects(self):
        response = self.client.get('/api/subjects/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results'] if 'results' in response.data else response.data
        self.assertGreaterEqual(len(results), 2)

    def test_only_published_questions_returned(self):
        response = self.client.get('/api/questions/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results'] if 'results' in response.data else response.data
        question_ids = [q['id'] for q in results]

        self.assertIn(self.pub_question.id, question_ids)
        self.assertNotIn(self.draft_question.id, question_ids)

    def test_filter_by_difficulty(self):
        response = self.client.get('/api/questions/?difficulty=easy')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results'] if 'results' in response.data else response.data
        for q in results:
            self.assertEqual(q['difficulty'], 'easy')

