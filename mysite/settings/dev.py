from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# DEBUG = False

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'g&nxd2pp%!$-6ftl#*hok9y0@lp^tou^yx3@=plrz62k2)708@'

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['*'] 

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
