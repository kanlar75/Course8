import os
from datetime import timedelta
from pathlib import Path
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ENV_TYPE = os.getenv('ENV_TYPE')
if ENV_TYPE == 'local' or ENV_TYPE == 'docker':
    ALLOWED_host = ['localhost']
elif ENV_TYPE == 'no_lockal' or ENV_TYPE == 'docker_deploy':
    ALLOWED_HOSTS = [os.getenv('ALLOWED_HOSTS')]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'rest_framework_simplejwt',
    'drf_yasg',
    'django_celery_beat',
    'corsheaders',

    'users',
    'habits',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'config.wsgi.application'

# host и redis зависят от того где и как запускается проект смотри .env.sample

if ENV_TYPE == 'local':
    host = 'localhost'
    redis_host = '127.0.0.1:6379'
elif ENV_TYPE == 'docker' or ENV_TYPE == 'docker_deploy':
    host = os.getenv('POSTGRES_HOST')
    redis_host = 'redis:6379/0'
else:
    redis_host = 'redis:6379/0'
    host = ''

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB'),
        'USER': os.getenv('POSTGRES_USER'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'PORT': os.getenv('POSTGRES_PORT'),
        'HOST': host

    }
}
# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation'
                '.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation'
                '.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation'
                '.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation'
                '.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True

# DATETIME_FORMAT = "%d.%m.%Y %H:%M"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

if ENV_TYPE == 'local':
    STATIC_URL = 'static/'
    STATICFILES_DIRS = (
        BASE_DIR / 'static/',
    )
else:
    STATIC_ROOT = BASE_DIR / 'static'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'users.USER'
# LOGIN_REDIRECT_URL = '/'
# LOGOUT_REDIRECT_URL = '/'
# LOGIN_URL = '/users'


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication'
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}
CORS_ALLOWED_ORIGINS = [
    "https://read-only.example.com",
    "https://read-and-write.example.com",
    "http://localhost:8000",

]

CSRF_TRUSTED_ORIGINS = [
    "https://read-and-write.example.com",
]

CORS_ALLOW_ALL_ORIGINS = False

# Настройки для Celery

CELERY_BROKER_URL = f'redis://{redis_host}'

CELERY_RESULT_BACKEND = f'redis://{redis_host}'

CELERY_TIMEZONE = "Europe/Moscow"

CELERY_TASK_TRACK_STARTED = True

CELERY_TASK_TIME_LIMIT = 30 * 60

CELERY_BEAT_SCHEDULE = {
    'task-name': {
        'task': 'send_message',
        'schedule': timedelta(seconds=30),
    }
}
TELEGRAM_TOKEN = os.getenv('TG_BOT_TOKEN')
