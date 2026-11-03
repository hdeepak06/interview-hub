from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class StudentProfile(models.Model):
    BRANCH_CHOICES = [
        ('CSE', 'Computer Science and Engineering'),
        ('ISE', 'Information Science and Engineering'),
        ('AIML', 'Artificial Intelligence and Machine Learning'),
        ('OTHER', 'Other Engineering Branch / Fresher'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    branch = models.CharField(max_length=20, choices=BRANCH_CHOICES, default='CSE')
    semester = models.PositiveSmallIntegerField(default=8)
    college_name = models.CharField(max_length=255, blank=True, default='')
    bio = models.TextField(blank=True, default='')
    target_role = models.CharField(max_length=100, blank=True, default='Software Engineer')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} ({self.branch})"

