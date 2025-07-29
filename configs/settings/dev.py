import os
from datetime import timedelta
from configs.settings.base import *

# Debug mode enabled for development
DEBUG = True

# Allow all hosts during development
ALLOWED_HOSTS = ['*']

# Database configuration using environment variables
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DEV_DB_NAME'),
        'USER': os.environ.get('DEV_DB_USER'),
        'PASSWORD': os.environ.get('DEV_DB_PASSWORD'),
        'HOST': os.environ.get('DEV_DB_HOST'),
        'PORT': os.environ.get('DEV_DB_PORT'),
    }
}

# CORS Configuration
CORS_ALLOW_ALL_ORIGINS = False

CORS_ALLOWED_ORIGINS = os.environ.get('DEV_CORS_ALLOWED_ORIGINS', '').split(',')

CORS_ALLOW_HEADERS = [
    "accept",
    "authorization",
    "content-type",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]

CORS_ALLOW_METHODS = [
    "GET",
    "POST",
    "PUT",
    "PATCH",
    "DELETE",
    "OPTIONS",
]

# JWT token settings
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=5),
}
