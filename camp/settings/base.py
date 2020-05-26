"""
Django settings for the Community Air Monitoring Project.

Generated by 'django-admin startproject' using Django 2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import subprocess

import dj_database_url

from django.utils.translation import gettext_lazy

from unipath import Path

# Build paths inside the project like this: BASE_DIR.child(...)
BASE_DIR = Path(__file__).absolute().ancestor(3)
PROJECT_DIR = Path(__file__).absolute().ancestor(2)

COMMIT_HASH = os.environ.get('HEROKU_SLUG_COMMIT')
if COMMIT_HASH is None:
    COMMIT_HASH = subprocess.check_output(
        ['git', 'rev-parse', '--short', 'HEAD']
    ).strip()

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(int(os.environ.get('DJANGO_DEBUG', 1)))

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost').split(',')


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.gis',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 'channels',
    # 'channels_redis',
    'corsheaders',
    'admin_honeypot',
    'django_extensions',
    'django_filters',
    'huey.contrib.djhuey',
    'livereload',
    'localflavor',
    'storages',

    'camp.api',
    'camp.apps.accounts',
    'camp.apps.monitors',
    'camp.apps.monitors.purpleair',
    'camp.apps.purple',
    'camp.apps.sensors',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'camp.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [PROJECT_DIR.child('templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'camp.context_processors.settings_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'camp.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': dj_database_url.config(
        engine='django.contrib.gis.db.backends.postgis'
    )
}


# Redis

REDIS_URL = None
for var in ["REDIS_URL", "OPENREDIS_URL"]:
    REDIS_URL = os.environ.get(var)
    if REDIS_URL is not None:
        break


# Auth

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

AUTH_USER_MODEL = 'accounts.User'


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LANGUAGE_CODE = 'en'

LANGUAGES = (
    ('en', gettext_lazy('English')),
)


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_ROOT = BASE_DIR.child('public', 'static')

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR.child('assets'),
    BASE_DIR.child('dist'),
]

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

MEDIA_ROOT = BASE_DIR.child('public', 'media')

MEDIA_URL = os.environ.get('MEDIA_URL', '/media/')


# django-cors-headers

CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOW_CREDENTIALS = True

# Google Maps

GOOGLE_MAPS_API_KEY = os.environ.get('GOOGLE_MAPS_API_KEY', '')

# django-resticus

RESTICUS = {
    'DEFAULT_AUTHENTICATION_CLASSES': [],
}


# huey

HUEY = {
    "connection": {"url": REDIS_URL},
    "consumer": {
        "periodic": True,
        "workers": int(os.environ.get('HUEY_WORKERS', 4))
    },
    "immediate": bool(int(os.environ.get('HUEY_IMMEDIATE', DEBUG)))
}
