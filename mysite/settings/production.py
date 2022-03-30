from .base import *
import dj_database_url

DATABASES['default'] = dj_database_url.config()

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# DEBUG = False

# SECURITY WARNING: keep the secret key used in production secret!
from __future__ import absolute_import, unicode_literals

import os

env = os.environ.copy()
SECRET_KEY = env['SECRET_KEY']

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


INSTALLED_APPS = INSTALLED_APPS + [
    # ...
    "debug_toolbar",
    "django_extensions",
    "wagtail.contrib.styleguide",
    # ...
]

MIDDLEWARE += [
    # ...
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    # ...
]

INTERNAL_IPS = [
    # ...
    "127.0.0.1",
    "172.17.0.1"
    # ...
]

CACHES = {
    "default":{
        "BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
        "LOCATION": "\\Users\B&B\PycharmProjects\pythonProject\mysite\cache"
    }
}


try:
    from .local import *
except ImportError:
    pass
