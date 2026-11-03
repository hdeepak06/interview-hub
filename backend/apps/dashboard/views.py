from rest_framework import views, permissions
from rest_framework.response import Response
from django.db.models import Sum, Count, Avg
from apps.assessments.models import TestAttempt
from apps.progress.models import Bookmark, StudentProgress, LearningActivity
from apps.progress.serializers import LearningActivitySerializer
from apps.content.models import Subject

class DashboardOverviewView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user

        # 1. Mock tests summary
        test_attempts = TestAttempt.objects.filter(student=user, is_completed=True)
        mock_tests_count = test_attempts.count()
        avg_score = test_attempts.aggregate(avg=Avg('score_percentage'))['avg'] or 0.0

        # 2. Questions attempted & accuracy from StudentProgress
        progress_records = StudentProgress.objects.filter(user=user)
        total_attempted = progress_records.aggregate(total=Sum('questions_attempted'))['total'] or 0
        total_correct = progress_records.aggregate(total=Sum('questions_correct'))['total'] or 0

        # Also add questions answered in mock test attempts
        test_questions = test_attempts.aggregate(
            total=Sum('total_questions'),
            correct=Sum('correct_answers')
        )
        total_attempted += (test_questions['total'] or 0)
        total_correct += (test_questions['correct'] or 0)

        accuracy = (total_correct / total_attempted * 100) if total_attempted > 0 else 0.0

        # 3. Difficulty distribution
        easy_correct = progress_records.aggregate(total=Sum('easy_correct'))['total'] or 0
        medium_correct = progress_records.aggregate(total=Sum('medium_correct'))['total'] or 0
        difficult_correct = progress_records.aggregate(total=Sum('difficult_correct'))['total'] or 0

        # 4. Subject-wise progress
        subjects_progress = []
        for p in progress_records:
            total_target = p.subject.target_questions or 100
            pct = min(100, int((p.questions_correct / total_target) * 100))
            subjects_progress.append({
                'name': p.subject.name,
                'slug': p.subject.slug,
                'solved_count': p.questions_correct,
                'total_count': total_target,
                'percentage': pct
            })

        # 5. Bookmarks count
        bookmarks_count = Bookmark.objects.filter(user=user).count()

        # 6. Recent activities
        recent_acts = LearningActivity.objects.filter(user=user).order_by('-created_at')[:6]
        recent_acts_data = LearningActivitySerializer(recent_acts, many=True).data

        # 7. Learning streak (days active)
        # Compute distinct active dates
        distinct_days = LearningActivity.objects.filter(user=user)\
            .dates('created_at', 'day', order='DESC')
        streak_days = len(distinct_days)

        return Response({
            'status': 'success',
            'questions_attempted': total_attempted,
            'questions_correct': total_correct,
            'questions_incorrect': total_attempted - total_correct,
            'accuracy_percentage': round(accuracy, 1),
            'mock_tests_completed': mock_tests_count,
            'average_test_score': round(avg_score, 1),
            'bookmarks_count': bookmarks_count,
            'learning_streak_days': streak_days,
            'subjects_progress': subjects_progress,
            'difficulty_distribution': {
                'easy': easy_correct,
                'medium': medium_correct,
                'difficult': difficult_correct
            },
            'recent_activities': recent_acts_data
        })

