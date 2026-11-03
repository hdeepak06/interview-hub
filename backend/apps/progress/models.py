from django.db import models
from django.contrib.auth.models import User
from apps.content.models import Subject, Question

class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookmarks')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='bookmarked_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ('user', 'question')

    def __str__(self):
        return f"{self.user.username} saved Q{self.question_id}"

class StudentProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subject_progress')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    questions_attempted = models.PositiveIntegerField(default=0)
    questions_correct = models.PositiveIntegerField(default=0)

    easy_correct = models.PositiveIntegerField(default=0)
    medium_correct = models.PositiveIntegerField(default=0)
    difficult_correct = models.PositiveIntegerField(default=0)

    last_activity_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'subject')

    def __str__(self):
        return f"{self.user.username} - {self.subject.name}: {self.questions_correct}/{self.questions_attempted}"

class LearningActivity(models.Model):
    ACTIVITY_TYPE_CHOICES = [
        ('question_attempted', 'Question Attempted'),
        ('test_completed', 'Mock Test Completed'),
        ('problem_solved', 'Coding Problem Solved'),
        ('bookmark_added', 'Bookmark Added'),
    ]

    STATUS_CHOICES = [
        ('correct', 'Correct'),
        ('incorrect', 'Incorrect'),
        ('completed', 'Completed'),
        ('info', 'Info'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=50, choices=ACTIVITY_TYPE_CHOICES)
    title = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='completed')
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"[{self.activity_type}] {self.user.username}: {self.title}"

