from django.urls import path
from .views import GenerateMockTestView, SubmitMockTestView, TestAttemptHistoryView

urlpatterns = [
    path('mock-tests/generate/', GenerateMockTestView.as_view(), name='mock-test-generate'),
    path('mock-tests/submit/', SubmitMockTestView.as_view(), name='mock-test-submit'),
    path('mock-tests/attempts/', TestAttemptHistoryView.as_view(), name='mock-test-attempts'),
]

