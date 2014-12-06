DEBUG = True

ALLOWED_HOSTS = []

ADDITIONAL_INSTALLED_APPS = []
ADDITIONAL_MIDDLEWARE_CLASSES = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'miniprint_django',
    }
}

SECRET_KEY = 'MAKE_YOUR_SECRET_KEY_UNIQUE_AND_KEEP_IS_SAFE_BOOYA'
