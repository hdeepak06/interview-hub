from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookmarkViewSet, StudentProgressView

router = DefaultRouter()
router.register(r'bookmarks', BookmarkViewSet, basename='bookmark')

urlpatterns = [
    path('progress/', StudentProgressView.as_view(), name='student-progress'),
    path('', include(router.urls)),
]

