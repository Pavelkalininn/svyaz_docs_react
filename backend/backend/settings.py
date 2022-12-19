import os
from pathlib import (
    Path,
)
import backend.tasks

from celery.schedules import crontab
from dotenv import (
    load_dotenv,
)

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv()


SECRET_KEY = os.getenv('SECRET_KEY', default='tokentokentokentokentokentokentokentokentokent')
DEBUG = True

CELERY_BROKER_URL = 'redis://redis:6379'
CELERY_RESULT_BACKEND = 'redis://redis:6379'

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',
    'django_filters',
    'djoser',
    'documents',
    'api'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

]

CORS_ALLOW_CREDENTIALS = True
CSRF_COOKIE_NAME = "csrftoken"
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'http://127.0.0.1:3000'
]
ROOT_URLCONF = 'backend.urls'
CSRF_TRUSTED_ORIGINS = ['127.0.0.1:3000', 'localhost:3000']

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['static'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'backend.wsgi.application'

# DATABASES = {
#     'default': {
#         'ENGINE': os.getenv('DB_ENGINE', default='django.db.backends.postgresql'),
#         'NAME': os.getenv('DB_NAME', default='postgres'),
#         'USER': os.getenv('POSTGRES_USER', default='postgres'),
#         'PASSWORD': os.getenv('POSTGRES_PASSWORD', default='postgres'),
#         'HOST': os.getenv('DB_HOST', default='localhost'),
#         'PORT': os.getenv('DB_PORT', default='5432'),
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]
LANGUAGE_CODE = 'ru-RU'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
INITIALS_REGEX = r'^[A-ZА-ЯЁ][a-zа-яё]+ [A-ZА-ЯЁ]\.(?:[A-ZА-ЯЁ]\.|)\Z'
FULL_NAME_REGEX = (
    r'^[A-ZА-ЯЁ][a-zа-яё]+ [A-ZА-ЯЁ][a-zа-яё]+(?: [A-ZА-ЯЁ][a-zа-яё]+|)\Z'
)
PHONE_REGEX = r'^\+[0-9]{10,18}\Z'
EMAIL_REGEX = r'^.{2,}@.{2,}\..{2,}\Z'
GTIN_REGEX = r'^[0-9]{8,14}\Z'

USER_ROLE_CHOICES = (
    ('user', 'USER'),
    ('staff', 'STAFF'),
    ('admin', 'ADMIN'),
)

CHAR_FIELD_MAX_SIZE = 255
CHAR_FIELD_MIDDLE_SIZE = 127
CHAR_FIELD_SMALL_SIZE = 40
CHAR_FIELD_PHONE_SIZE = 18

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
}
AUTH_USER_MODEL = 'documents.User'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


CELERY_BEAT_SCHEDULE = {
    'remove_temp_files_task': {
        'task': 'backend.tasks.remove_temp_files_task',
        'schedule': crontab(minute='*/1'),
    },
}
