import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DEBUG = True

ALLOWED_HOSTS = []

ADDITIONAL_INSTALLED_APPS = []
ADDITIONAL_MIDDLEWARE_CLASSES = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'miniprint.sqlite3'),
    }
}

SECRET_KEY = 'MAKE_YOUR_SECRET_KEY_UNIQUE_AND_KEEP_IS_SAFE_BOOYA'
