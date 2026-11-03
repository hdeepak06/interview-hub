from rest_framework import serializers
from .models import Subject, Topic, Question, AnswerOption, QuestionReview

class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ['id', 'name', 'slug', 'description', 'display_order']

class SubjectSerializer(serializers.ModelSerializer):
    topics = TopicSerializer(many=True, read_only=True)
    published_questions_count = serializers.SerializerMethodField()

    class Meta:
        model = Subject
        fields = [
            'id', 'name', 'slug', 'description', 'icon', 
            'target_questions', 'display_order', 'topics', 'published_questions_count'
        ]

    def get_published_questions_count(self, obj):
        return obj.questions.filter(review_status='published', is_active=True).count()

class AnswerOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerOption
        fields = ['id', 'option_label', 'option_text']

class AnswerOptionDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerOption
        fields = ['id', 'option_label', 'option_text', 'is_correct', 'explanation']

class QuestionSerializer(serializers.ModelSerializer):
    subject_name = serializers.ReadOnlyField(source='subject.name')
    subject_slug = serializers.ReadOnlyField(source='subject.slug')
    topic_name = serializers.ReadOnlyField(source='topic.name')
    options = AnswerOptionSerializer(many=True, read_only=True)
    is_bookmarked = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = [
            'id', 'subject', 'subject_name', 'subject_slug', 'topic', 'topic_name',
            'difficulty', 'question_type', 'question_text', 'correct_answer',
            'explanation', 'practical_example', 'code_example', 'expected_output',
            'interview_tip', 'tags', 'options', 'is_bookmarked'
        ]

    def get_is_bookmarked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            from apps.progress.models import Bookmark
            return Bookmark.objects.filter(user=request.user, question=obj).exists()
        return False

