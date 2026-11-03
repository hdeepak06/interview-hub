from django.db import models
from django.contrib.auth.models import User
from apps.content.models import Subject, Question

class MockTest(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('difficult', 'Difficult'),
        ('mixed', 'Mixed Difficulties'),
    ]

    title = models.CharField(max_length=200)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True, related_name='mock_tests')
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='medium')
    question_count = models.PositiveIntegerField(default=15)
    time_limit_minutes = models.PositiveIntegerField(default=20)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.time_limit_minutes}m)"

class MockTestQuestion(models.Model):
    mock_test = models.ForeignKey(MockTest, on_delete=models.CASCADE, related_name='test_questions')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    question_order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['question_order']
        unique_together = ('mock_test', 'question')

class TestAttempt(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='test_attempts')
    mock_test = models.ForeignKey(MockTest, on_delete=models.SET_NULL, null=True, blank=True)
    subject_slug = models.CharField(max_length=100, default='general')

    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    total_questions = models.PositiveIntegerField(default=0)
    correct_answers = models.PositiveIntegerField(default=0)
    incorrect_answers = models.PositiveIntegerField(default=0)
    unanswered = models.PositiveIntegerField(default=0)

    score_percentage = models.FloatField(default=0.0)
    time_taken_seconds = models.PositiveIntegerField(default=0)
    is_completed = models.BooleanField(default=False)

    class Meta:
        ordering = ['-started_at']

    def __str__(self):
        return f"{self.student.username} - {self.subject_slug} ({self.score_percentage:.1f}%)"

class TestResponse(models.Model):
    attempt = models.ForeignKey(TestAttempt, on_delete=models.CASCADE, related_name='responses')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option_label = models.CharField(max_length=10, blank=True, default='')
    is_correct = models.BooleanField(default=False)
    time_spent_seconds = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Attempt {self.attempt_id} - Q{self.question_id}: {'✓' if self.is_correct else '✕'}"

