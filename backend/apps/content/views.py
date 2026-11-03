from rest_framework import viewsets, permissions, filters
from .models import Subject, Topic, Question
from .serializers import SubjectSerializer, TopicSerializer, QuestionSerializer

class SubjectViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Subject.objects.filter(is_active=True).prefetch_related('topics')
    serializer_class = SubjectSerializer
    lookup_field = 'slug'
    permission_classes = [permissions.AllowAny]

class TopicViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Topic.objects.filter(is_active=True)
    serializer_class = TopicSerializer
    permission_classes = [permissions.AllowAny]

class QuestionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = QuestionSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = Question.objects.filter(review_status='published', is_active=True)\
            .select_related('subject', 'topic')\
            .prefetch_related('options')

        subject = self.request.query_params.get('subject')
        if subject:
            queryset = queryset.filter(subject__slug=subject)

        difficulty = self.request.query_params.get('difficulty')
        if difficulty:
            queryset = queryset.filter(difficulty=difficulty.lower())

        topic = self.request.query_params.get('topic')
        if topic:
            queryset = queryset.filter(topic__slug=topic)

        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(question_text__icontains=search)

        limit = self.request.query_params.get('limit')
        if limit and limit.isdigit():
            queryset = queryset[:int(limit)]

        return queryset
