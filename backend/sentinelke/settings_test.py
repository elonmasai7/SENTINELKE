from .settings import *

EXCLUDED_APPS = {
    'django.contrib.gis',
    'apps.geo',
    'apps.operations',
    'apps.field_ops',
}

INSTALLED_APPS = [app for app in INSTALLED_APPS if app not in EXCLUDED_APPS]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'test.sqlite3',
    }
}

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
ROOT_URLCONF = 'sentinelke.urls_test'
CHANNEL_LAYERS = {'default': {'BACKEND': 'channels.layers.InMemoryChannelLayer'}}
