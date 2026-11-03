from rest_framework import serializers
from .models import MockTest, TestAttempt, TestResponse
from apps.content.models import Question, AnswerOption

class SafeAnswerOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerOption
        fields = ['id', 'option_label', 'option_text']

class AssessmentQuestionSerializer(serializers.ModelSerializer):
    options = SafeAnswerOptionSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = [
            'id', 'difficulty', 'question_type', 'question_text',
            'code_example', 'options'
        ]

class TestAttemptSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestAttempt
        fields = '__all__'

