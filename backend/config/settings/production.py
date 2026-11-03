"""
Production settings for Deepak Interview Hub.
Learn. Practise. Test. Get Interview Ready.
"""

from .base import *
import os

DEBUG = os.environ.get('DEBUG', 'False').lower() in ('true', '1')

SECRET_KEY = os.environ.get(
    'DJANGO_SECRET_KEY', 
    'django-prod-fallback-secret-key-change-in-production-vault-99281729'
)

# Allow Vercel preview and production domains automatically
ALLOWED_HOSTS = os.environ.get(
    'ALLOWED_HOSTS', 
    '*'
).split(',')

# Support PostgreSQL when configured; fall back gracefully to SQLite for serverless/build
if os.environ.get('DB_NAME') and os.environ.get('DB_USER'):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('DB_NAME'),
            'USER': os.environ.get('DB_USER'),
            'PASSWORD': os.environ.get('DB_PASSWORD', ''),
            'HOST': os.environ.get('DB_HOST', 'localhost'),
            'PORT': os.environ.get('DB_PORT', '5432'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Production Security Headers (enable SSL redirect only if configured or HTTPS header present)
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = os.environ.get('SECURE_SSL_REDIRECT', 'False').lower() in ('true', '1')
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

