from rest_framework import views, status, permissions
from rest_framework.response import Response
from django.utils import timezone
from .models import MockTest, TestAttempt, TestResponse
from .serializers import AssessmentQuestionSerializer, TestAttemptSerializer
from apps.content.models import Subject, Question, AnswerOption
from apps.progress.models import StudentProgress, LearningActivity

class GenerateMockTestView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        subject_slug = request.data.get('subject', 'python')
        difficulty = request.data.get('difficulty')
        count = int(request.data.get('question_count', 15))

        queryset = Question.objects.filter(review_status='published', is_active=True)

        if subject_slug and subject_slug != 'all':
            queryset = queryset.filter(subject__slug=subject_slug)

        if difficulty and difficulty in ['easy', 'medium', 'difficult']:
            queryset = queryset.filter(difficulty=difficulty)

        # Order by id or random
        questions = queryset.order_by('?')[:count]
        if not questions.exists():
            # If not enough filtered by difficulty, broaden
            questions = Question.objects.filter(subject__slug=subject_slug, review_status='published')[:count]

        attempt_id = f"test_{int(timezone.now().timestamp())}"

        serializer = AssessmentQuestionSerializer(questions, many=True)
        return Response({
            'status': 'success',
            'attempt_id': attempt_id,
            'subject': subject_slug,
            'count': len(serializer.data),
            'questions': serializer.data
        })

class SubmitMockTestView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        answers = request.data.get('answers', {}) # { "question_id": "A" or option_id }
        subject_slug = request.data.get('subject', 'general')
        time_taken = int(request.data.get('time_taken_seconds', 0))

        question_ids = list(answers.keys())
        questions = Question.objects.filter(id__in=question_ids).prefetch_related('options')

        correct_count = 0
        total_questions = len(question_ids)
        review_details = []

        for q in questions:
            user_choice = str(answers.get(str(q.id)) or answers.get(q.id))
            correct_opt = q.options.filter(is_correct=True).first()
            correct_label = correct_opt.option_label if correct_opt else q.correct_answer

            is_correct = (user_choice == correct_label)

            if is_correct:
                correct_count += 1

            review_details.append({
                'id': q.id,
                'question_text': q.question_text,
                'user_answer': user_choice,
                'correct_answer': correct_label,
                'is_correct': is_correct,
                'explanation': q.explanation
            })

        score_percentage = (correct_count / total_questions * 100) if total_questions > 0 else 0

        # If authenticated, persist to database and update progress
        if request.user.is_authenticated:
            attempt = TestAttempt.objects.create(
                student=request.user,
                subject_slug=subject_slug,
                total_questions=total_questions,
                correct_answers=correct_count,
                incorrect_answers=total_questions - correct_count,
                score_percentage=score_percentage,
                time_taken_seconds=time_taken,
                is_completed=True,
                completed_at=timezone.now()
            )

            # Log learning activity
            LearningActivity.objects.create(
                user=request.user,
                activity_type='test_completed',
                title=f"Completed {subject_slug.upper()} Mock Test",
                metadata={'score': score_percentage, 'correct': correct_count, 'total': total_questions}
            )

        return Response({
            'status': 'success',
            'subject': subject_slug,
            'total_questions': total_questions,
            'correct_count': correct_count,
            'incorrect_count': total_questions - correct_count,
            'score_percentage': round(score_percentage, 1),
            'time_taken_seconds': time_taken,
            'questions': review_details
        })

class TestAttemptHistoryView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        attempts = TestAttempt.objects.filter(student=request.user).order_by('-started_at')[:20]
        serializer = TestAttemptSerializer(attempts, many=True)
        return Response({
            'status': 'success',
            'results': serializer.data
        })

