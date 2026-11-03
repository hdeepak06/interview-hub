from django.db import models
from django.contrib.auth.models import User

class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True, default='')
    icon = models.CharField(max_length=50, default='📚')
    target_questions = models.PositiveIntegerField(default=100)
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['display_order', 'name']

    def __str__(self):
        return self.name

class Topic(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='topics')
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150)
    description = models.TextField(blank=True, default='')
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['display_order', 'name']
        unique_together = ('subject', 'slug')

    def __str__(self):
        return f"{self.subject.name} - {self.name}"

class Question(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('difficult', 'Difficult'),
    ]

    QUESTION_TYPE_CHOICES = [
        ('mcq', 'Multiple Choice Question'),
        ('short_answer', 'Short Answer'),
        ('descriptive', 'Descriptive / Conceptual'),
    ]

    REVIEW_STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('reviewed', 'Reviewed'),
        ('approved', 'Approved'),
        ('published', 'Published'),
    ]

    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='questions')
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True, blank=True, related_name='questions')
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='medium', db_index=True)
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPE_CHOICES, default='mcq')

    question_text = models.TextField()
    correct_answer = models.TextField()
    explanation = models.TextField()
    practical_example = models.TextField(blank=True, default='')
    code_example = models.TextField(blank=True, default='')
    expected_output = models.TextField(blank=True, default='')
    interview_tip = models.TextField(blank=True, default='')
    tags = models.JSONField(default=list, blank=True)

    review_status = models.CharField(max_length=20, choices=REVIEW_STATUS_CHOICES, default='published', db_index=True)
    is_active = models.BooleanField(default=True, db_index=True)

    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_questions')
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_questions')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f"[{self.subject.slug.upper()}] {self.question_text[:60]}"

class AnswerOption(models.Model):
    OPTION_LABEL_CHOICES = [
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
    ]

    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    option_label = models.CharField(max_length=5, choices=OPTION_LABEL_CHOICES)
    option_text = models.CharField(max_length=500)
    is_correct = models.BooleanField(default=False)
    explanation = models.TextField(blank=True, default='')

    class Meta:
        ordering = ['option_label']
        unique_together = ('question', 'option_label')

    def __str__(self):
        return f"{self.question.id} ({self.option_label}): {self.option_text[:40]}"

class QuestionReview(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=Question.REVIEW_STATUS_CHOICES)
    comments = models.TextField(blank=True, default='')
    reviewed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review #{self.id} on Question {self.question_id} by {self.reviewer.username}"

