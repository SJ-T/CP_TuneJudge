import environ
import os
import dj_database_url

from pathlib import Path


# Core Django Settings
BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))
SECRET_KEY = os.environ.get('SECRET_KEY')
DEBUG = os.environ.get('DEBUG', False)
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost 127.0.0.1').split(' ')
ROOT_URLCONF = 'core.urls'
WSGI_APPLICATION = 'core.wsgi.application'

# Application Settings
INSTALLED_APPS = [
    'corsheaders',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app.apps.AppConfig',
    'rest_framework',
    'storages',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Database Configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}
if 'DATABASE_URL' in os.environ:
    DATABASE_URL = os.environ.get('DATABASE_URL')
    DATABASES['default'] = dj_database_url.parse(DATABASE_URL)

if os.environ.get('USE_GCS', 'false').lower() == 'true':
    DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
    GS_BUCKET_NAME = os.environ.get('GS_BUCKET_NAME', None)
    GS_PROJECT_ID = os.environ.get('GS_PROJECT_ID', None)
    GS_CREDENTIALS = os.environ.get('GS_CREDENTIALS', None)
    from google.oauth2 import service_account
    GS_CREDENTIALS = service_account.Credentials.from_service_account_file(GS_CREDENTIALS)
else:
    DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Static Files Configuration
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
STORAGES = {
    'default': {'BACKEND': DEFAULT_FILE_STORAGE},
    'staticfiles': {'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage'},
}

# Security Settings
SECURE_SSL_REDIRECT = not DEBUG
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_SECONDS = 86400
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# API and CORS Settings
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '50/day',
    }
}
CORS_ALLOWED_ORIGINS = [
    origin.strip()
    for origin in os.environ.get('CORS_ALLOWED_ORIGINS', 'http://localhost:8501').split(',')
]
CORS_ALLOW_METHODS = [
    'GET',
    'POST',
    'OPTIONS',
]
CORS_EXPOSE_HEADERS = ['Content-Type']
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'content-type',
    'origin',
    'user-agent',
]
API_BASE_URL = os.environ.get('API_BASE_URL', 'http://localhost:8000/api/')

# Application-Specific Settings
DATASET_FEATURES_PATH = os.environ.get('DATASET_FEATURES_PATH', None)
EXP_FEATURES_PATH = os.environ.get('EXP_FEATURES_PATH', None)
WAV_FILE_PATH = os.environ.get('WAV_FILE_PATH', None)

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Admin Settings
SUPER_USER = os.environ.get('SUPER_USER', None)
SUPER_EMAIL = os.environ.get('SUPER_EMAIL', None)
SUPER_PASS = os.environ.get('SUPER_PASS', None)
