"""
Django settings for miniprint project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Simple but better way to deal with settings_local (without messing about with env)
try:
    from . import settings_local
except ImportError:
    from . import settings_local_empty as settings_local

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = settings_local.SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = settings_local.DEBUG

TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = settings_local.ALLOWED_HOSTS


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'adminsortable',
    'mptt',
    'twython_django_oauth',

    'users',
    'fineprint',
    'discuss',
    'web',
] + settings_local.ADDITIONAL_INSTALLED_APPS

MIDDLEWARE_CLASSES = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
] + settings_local.ADDITIONAL_MIDDLEWARE_CLASSES

ROOT_URLCONF = 'miniprint.urls'

WSGI_APPLICATION = 'miniprint.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = settings_local.DATABASES


# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATICFILES_DIRS = [  # REMOVE ME: this is only for PyCharm...
    os.path.join(BASE_DIR, 'web', 'static'),
]

# Media

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# User model

AUTH_USER_MODEL = 'users.User'


# Social auth

TWITTER_KEY = 'L5ZXu2ra4fged1CUONh8NMCyi'
TWITTER_SECRET = 'LSNWo1FRnOqIdiN10y9Zv6vpJT9e9XAIde20et2ChP79xb4S6d'

LOGIN_URL = '/twitter/login'
LOGOUT_URL = '/twitter/logout'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# Datetime formats
DATETIME_FORMAT = r'F jS Y \a\t H:i'
DATE_FORMAT = 'F jS Y'
SHORT_DATE_FORMAT = 'M j y'
SHORT_DATETIME_FORMAT = 'M j y H:i'
