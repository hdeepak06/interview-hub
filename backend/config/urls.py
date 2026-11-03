"""
Root URL Configuration for Deepak Interview Hub.
"""

from django.contrib import admin
from django.urls import path, re_path, include
from django.views.static import serve
from django.conf import settings

FRONTEND_DIR = settings.BASE_DIR / 'frontend'
if not FRONTEND_DIR.exists():
    FRONTEND_DIR = settings.BASE_DIR.parent / 'frontend'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('apps.accounts.urls')),
    path('api/', include('apps.content.urls')),
    path('api/', include('apps.practice.urls')),
    path('api/', include('apps.assessments.urls')),
    path('api/', include('apps.progress.urls')),
    path('api/', include('apps.dashboard.urls')),

    # Serve Frontend static assets & HTML pages
    path('', serve, {'document_root': FRONTEND_DIR, 'path': 'index.html'}, name='home'),
    re_path(r'^(?P<path>.*)$', serve, {'document_root': FRONTEND_DIR}),
]


