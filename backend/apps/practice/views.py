from rest_framework import viewsets, permissions
from .models import CodingProblem, SQLExercise
from .serializers import CodingProblemSerializer, SQLExerciseSerializer

class CodingProblemViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CodingProblem.objects.filter(is_active=True)
    serializer_class = CodingProblemSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'slug'

class SQLExerciseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SQLExercise.objects.filter(is_active=True)
    serializer_class = SQLExerciseSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'slug'

