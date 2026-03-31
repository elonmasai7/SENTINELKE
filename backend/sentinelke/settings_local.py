from .settings import *

EXCLUDED_APPS = {
    'django.contrib.gis',
    'apps.geo',
    'apps.field_ops',
}
INSTALLED_APPS = [app for app in INSTALLED_APPS if app not in EXCLUDED_APPS]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'local.sqlite3',
    }
}

SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
ROOT_URLCONF = 'sentinelke.urls_local'
CHANNEL_LAYERS = {'default': {'BACKEND': 'channels.layers.InMemoryChannelLayer'}}
