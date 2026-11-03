"""
Development settings for Deepak Interview Hub.
Uses SQLite for local testing without requiring local PostgreSQL daemon.
"""

from .base import *

DEBUG = True

SECRET_KEY = 'django-insecure-deepak-interview-hub-dev-secret-key-change-in-prod'

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

