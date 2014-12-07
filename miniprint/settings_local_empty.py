DEBUG = True

ALLOWED_HOSTS = []

ADDITIONAL_INSTALLED_APPS = []
ADDITIONAL_MIDDLEWARE_CLASSES = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'miniprint.sqlite3',
    }
}

SECRET_KEY = 'MAKE_YOUR_SECRET_KEY_UNIQUE_AND_KEEP_IS_SAFE_BOOYA'
