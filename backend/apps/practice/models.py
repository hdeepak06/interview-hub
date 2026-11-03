from django.db import models
from apps.content.models import Topic

class CodingProblem(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('difficult', 'Difficult'),
    ]

    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True, blank=True, related_name='coding_problems')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='easy')

    problem_statement = models.TextField()
    constraints = models.TextField(blank=True, default='')
    input_format = models.TextField(blank=True, default='')
    output_format = models.TextField(blank=True, default='')
    sample_input = models.TextField()
    sample_output = models.TextField()
    hint = models.TextField(blank=True, default='')

    reference_solution = models.TextField()
    algorithm_explanation = models.TextField()
    time_complexity = models.CharField(max_length=50, default='O(n)')
    space_complexity = models.CharField(max_length=50, default='O(1)')
    edge_cases = models.JSONField(default=list, blank=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"[{self.difficulty.upper()}] {self.title}"

class SQLExercise(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('difficult', 'Difficult'),
    ]

    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True, blank=True, related_name='sql_exercises')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='easy')

    database_schema = models.TextField(help_text="DDL statements or schema representation")
    sample_records = models.TextField(blank=True, default='')
    query_requirement = models.TextField()
    correct_sql = models.TextField()
    expected_output = models.TextField()
    explanation = models.TextField()

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"[{self.difficulty.upper()}] {self.title}"

