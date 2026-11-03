from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CodingProblemViewSet, SQLExerciseViewSet

router = DefaultRouter()
router.register(r'coding-problems', CodingProblemViewSet, basename='coding-problem')
router.register(r'sql-exercises', SQLExerciseViewSet, basename='sql-exercise')

urlpatterns = [
    path('', include(router.urls)),
]

