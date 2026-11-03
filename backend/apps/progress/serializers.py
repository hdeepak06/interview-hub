from rest_framework import serializers
from .models import Bookmark, StudentProgress, LearningActivity
from apps.content.models import Question

class BookmarkSerializer(serializers.ModelSerializer):
    question_text = serializers.ReadOnlyField(source='question.question_text')
    subject_name = serializers.ReadOnlyField(source='question.subject.name')
    difficulty = serializers.ReadOnlyField(source='question.difficulty')

    class Meta:
        model = Bookmark
        fields = ['id', 'question', 'question_text', 'subject_name', 'difficulty', 'created_at']
        read_only_fields = ['id', 'created_at']

    def create(self, validated_data):
        user = self.context['request'].user
        question = validated_data['question']
        bookmark, created = Bookmark.objects.get_or_create(user=user, question=question)
        return bookmark

class StudentProgressSerializer(serializers.ModelSerializer):
    subject_name = serializers.ReadOnlyField(source='subject.name')
    subject_slug = serializers.ReadOnlyField(source='subject.slug')

    class Meta:
        model = StudentProgress
        fields = '__all__'

class LearningActivitySerializer(serializers.ModelSerializer):
    timestamp = serializers.SerializerMethodField()

    class Meta:
        model = LearningActivity
        fields = ['id', 'activity_type', 'title', 'status', 'timestamp', 'created_at']

    def get_timestamp(self, obj):
        return obj.created_at.strftime("%b %d, %Y %I:%M %p")

