"""
Django settings for AIC22_Backend project.

Generated by 'django-admin startproject' using Django 3.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
from decouple import config

import os

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

SENTRY_ENABLED = os.getenv('SENTRY_ENABLED', 'False') == 'True'
SENTRY_DSN = os.getenv('SENTRY_DSN', 'https://sentry.aichallenge.ir/2')

if SENTRY_ENABLED:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[
            DjangoIntegration(),
        ],

        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # We recommend adjusting this value in production.
        traces_sample_rate=1.0,

        # If you wish to associate users to errors (assuming you are using
        # django.contrib.auth) you may enable sending PII data.
        send_default_pii=True
    )


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-ko^^x2))7s(n#ypjs+eakp^-#kf@ku=^07k!p8lfu4zl$w91o3'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG", 'True') == 'True'

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_tracking',
    'corsheaders',
    'drf_spectacular',
    'allauth',
    'website',
    'drf_yasg',
    'django.contrib.sites',
    'django_filters',
    'django_summernote',
    'communication',
    'account',
    'team',
    'challenge',
    'django_crontab',
    'infra_gateway',
]

# X_FRAME_OPTIONS = 'SAMEORIGIN'
SITE_ID = 1

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ALLOW_ALL_ORIGINS = config('CORS_ALLOW_ALL_ORIGINS', default=True, cast=bool)

ROOT_URLCONF = 'AIC22_Backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
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

WSGI_APPLICATION = 'AIC22_Backend.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': str(BASE_DIR / "db.sqlite3"),
#     }
# }

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": config('DB_NAME'),
        "USER": config('DB_USER'),
        "PASSWORD": config('DB_PASSWORD'),
        "HOST": config('DB_HOST'),
        "PORT": config('DB_PORT'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Tehran'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.environ.get('STATIC_ROOT', os.path.join(BASE_DIR, 'static_files'))

MEDIA_ROOT = (
    os.environ.get('MEDIA_ROOT', os.path.join(BASE_DIR, 'media'))
)

MEDIA_URL = '/media/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'account.User'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

# should be placed in .env file later
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
AIC_BACKEND_DOMAIN = config("AIC_BACKEND_DOMAIN", 'https://api.aichallenge.ir')
AIC_GATEWAY_DOMAIN = config("AIC_GATEWAY_DOMAIN", "https://gateway.aichallenge.ir")
AIC_DOMAIN = config("AIC_DOMAIN", 'https://aichallenge.ir')
EMAIL_HOST = config("EMAIL_HOST", 'smtp.gmail.com')
EMAIL_PORT = config("EMAIL_PORT", 587)
EMAIL_HOST_USER = config("EMAIL_HOST_USER", 'aic22test@gmail.com')
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", 'wzxmjcqftxmuhggu')

IS_PRODUCTION = config("ENVIRONMENT", "stg") == 'prod'


UPLOAD_PATHS = {
    'MAP': '',
    'MATCH_LOGS': '',
    'CLAN_IMAGE': ''
}

CRONJOBS = [
    ('* * * * *', 'website.cron.handle')
]

INFRA_GATEWAY_HOST = os.getenv('INFRA_GATEWAY_HOST', 'gateway.aichallenge.ir')
INFRA_GATEWAY_AUTH_TOKEN = os.getenv('INFRA_GATEWAY_AUTH_TOKEN', 'a2lydG96ZW5kZWdp')
SUBMISSION_COOLDOWN_IN_MINUTES = int(os.getenv('SUBMISSION_COOLDOWN_IN_MINUTES', '5'))
RABBITMQ_BROKER = os.getenv('RABBITMQ_BROKER', 'amqp://aic2022:aichallenge2022@188.121.111.163:5672')
INFRA_TOKEN = os.getenv('INFRA_TOKEN', 'a2lydG96ZW5kZWdp')
