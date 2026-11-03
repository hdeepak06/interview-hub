from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from apps.content.models import Subject, Question, AnswerOption
from apps.assessments.models import TestAttempt

class MockTestAssessmentTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='test_student', password='Password123!')
        self.client.force_authenticate(user=self.user)

        self.subject = Subject.objects.create(name='Python', slug='python')

        self.q1 = Question.objects.create(
            subject=self.subject,
            difficulty='easy',
            question_text='Which keyword is used to define a function in Python?',
            correct_answer='def',
            explanation='def is the keyword used to define a function.',
            review_status='published'
        )
        AnswerOption.objects.create(question=self.q1, option_label='A', option_text='func', is_correct=False)
        AnswerOption.objects.create(question=self.q1, option_label='B', option_text='def', is_correct=True)

        self.q2 = Question.objects.create(
            subject=self.subject,
            difficulty='easy',
            question_text='Is a Python tuple mutable or immutable?',
            correct_answer='Immutable',
            explanation='Tuples cannot be modified after instantiation.',
            review_status='published'
        )
        AnswerOption.objects.create(question=self.q2, option_label='A', option_text='Mutable', is_correct=False)
        AnswerOption.objects.create(question=self.q2, option_label='B', option_text='Immutable', is_correct=True)

    def test_generate_assessment_does_not_leak_correct_answers(self):
        response = self.client.post('/api/mock-tests/generate/', {
            'subject': 'python',
            'question_count': 2
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        questions = response.data['questions']
        self.assertGreaterEqual(len(questions), 1)

        # Ensure correct_answer is NOT exposed in the payload
        for q in questions:
            self.assertNotIn('correct_answer', q)
            self.assertNotIn('explanation', q)
            for opt in q['options']:
                self.assertNotIn('is_correct', opt)

    def test_submit_assessment_scores_accurately_server_side(self):
        # Student submits 1 correct (B) and 1 incorrect (A)
        payload = {
            'subject': 'python',
            'answers': {
                str(self.q1.id): 'B',  # Correct
                str(self.q2.id): 'A',  # Incorrect
            },
            'time_taken_seconds': 120
        }
        response = self.client.post('/api/mock-tests/submit/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_questions'], 2)
        self.assertEqual(response.data['correct_count'], 1)
        self.assertEqual(response.data['score_percentage'], 50.0)

        # Check that TestAttempt was saved in the database
        attempt = TestAttempt.objects.filter(student=self.user).first()
        self.assertIsNotNone(attempt)
        self.assertEqual(attempt.correct_answers, 1)
        self.assertEqual(attempt.score_percentage, 50.0)

