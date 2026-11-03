from rest_framework import viewsets, permissions, views, status
from rest_framework.response import Response
from .models import Bookmark, StudentProgress, LearningActivity
from .serializers import BookmarkSerializer, StudentProgressSerializer

class BookmarkViewSet(viewsets.ModelViewSet):
    serializer_class = BookmarkSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Bookmark.objects.filter(user=self.request.user).select_related('question__subject')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class StudentProgressView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        progress = StudentProgress.objects.filter(user=request.user).select_related('subject')
        serializer = StudentProgressSerializer(progress, many=True)
        return Response({
            'status': 'success',
            'results': serializer.data
        })

