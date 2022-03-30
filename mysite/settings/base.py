"""
Django settings for mysite project.

Generated by 'django-admin startproject' using Django 3.1.14.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(PROJECT_DIR)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/


# Application definition

INSTALLED_APPS = [
    'home',
    'search',
    'flex',
    'streams',
    'site_settings',
    'subscribers',
    'blog',
    'menuss',
    'contact',
    'core',

    'wagtail.contrib.forms',
    'wagtail.contrib.modeladmin',
    'wagtail.contrib.redirects',
    'wagtail.contrib.settings',
    'wagtail.contrib.routable_page',
    'wagtail.contrib.sitemaps',
    'wagtail.embeds',
    'wagtail.sites',
    'wagtail.users',
    'wagtail.snippets',
    'wagtail.documents',
    'wagtail.images',
    'wagtail.search',
    'wagtail.admin',
    'wagtail.core',
    'wagtail.api.v2',

    'modelcluster',
    'taggit',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'django.contrib.sites',

    'captcha',
    'wagtailcaptcha',
    'rest_framework',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
]

LOGIN_REDIRECT_URL = '/'

SITE_ID = 1


# SOCIALACCOUNT_PROVIDERS = {
#     'google': {
#         'APP': {
#             'client_id': '189817624536-uqe18nasupvdkjfm6u54ng2rh9bks99j.apps.googleusercontent.com',
#             'secret': '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',
#             # 'client_id': '189817624536-e5i1n78ndr6tq490edr0fm3ubsi9n590.apps.googleusercontent.com',
#             # 'secret': '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',
#             'key': ''
#         },
#         'SCOPE': [
#             'profile',
#             'email',
#         ],
#         'AUTH_PARAMS': {
#             'access_type': 'online',
#         }
#     }
# }



SOCIALACCOUNT_PROVIDERS = {
    'google': {
        # For each OAuth based provider, either add a ``SocialApp``
        # (``socialaccount`` app) containing the required client
        # credentials, or list them here:
        'APP': {
            'client_id': '730899804760-p95qprlbge5onp2d7b9ekv1jet8fbv8t.apps.googleusercontent.com',
            'secret': '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',
            'key': ''
        }
    }
}



MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',

    'wagtail.contrib.redirects.middleware.RedirectMiddleware',
]

ROOT_URLCONF = 'mysite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(PROJECT_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'wagtail.contrib.settings.context_processors.settings',
            ],
        },
    },
]


AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',
    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
    # 'django_openid_auth.auth.OpenIDBackend',
    # 'social_core.backends.google.GoogleOAuth2',
]

WSGI_APPLICATION = 'mysite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'wagtail',
        'USER': 'wagtailankit',
        'PASSWORD': 'wagtailpwd',
        'HOST': 'localhost',  # Set to empty string for localhost.
        'PORT': '5432',  # Set to empty string for default.
        'CONN_MAX_AGE': 600,  # number of seconds database connections should persist for
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

STATICFILES_DIRS = [
    os.path.join(PROJECT_DIR, 'static'),
]

# ManifestStaticFilesStorage is recommended in production, to prevent outdated
# JavaScript / CSS assets being served from cache (e.g. after a Wagtail upgrade).
# See https://docs.djangoproject.com/en/3.1/ref/contrib/staticfiles/#manifeststaticfilesstorage
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'


# Wagtail settings

WAGTAIL_SITE_NAME = "mysite"

# Search
# https://docs.wagtail.io/en/stable/topics/search/backends.html
WAGTAILSEARCH_BACKENDS = {
    'default': {
        'BACKEND': 'wagtail.search.backends.database',
    }
}

# Base URL to use when referring to full URLs within the Wagtail admin backend -
# e.g. in notification emails. Don't include '/admin' or a trailing slash
BASE_URL = 'http://example.com'


#recptcha settings
RECAPTCHA_PUBLIC_KEY = "6LcEn4AeAAAAAJaWf6ODHer99ft5L1ZxIc70_jGA"
RECAPTCHA_PRIVATE_KEY = "6LcEn4AeAAAAAB68MP2yW-SU17zlVhzVvi5uPuIe"
NOCAPTCHA =True

# ACCOUNT_AUTHENTICATED_LOGIN_REDIRECTS = True
LOGIN_URL = '/LOGIN/'

ACCOUNT_AUTHENTICATION_METHOD = "username_email"
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_LOGOUT_ON_PASSWORD_CHANGE = True
ACCOUNT_LOGOUT_REDIRECT_URL = "/login"
ACCOUNT_PRESERVE_USERNAME_CASING = False
ACCOUNT_SESSION_REMEMBER = True
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = False
ACCOUNT_USERNAME_BLACKLIST = ["ankit","admin","god"]
ACCOUNT_USERNAME_MIN_LENGTH = 2



# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }
# DATABASES={
#    'default':{
#       'ENGINE':'django.db.backends.postgresql_psycopg2',
#       'NAME':'postgres',
#       'USER':'mydbuser',
#       'PASSWORD':'ankitwaskle',
#       'HOST':'localhost',
#       'PORT':'5432',
#    }
# }
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'newserver',
#         'USER': 'postgres',
#         'PASSWORD': 'newserver',
#         'HOST': 'localhost',  # Set to empty string for localhost.
#         'PORT': '5432',  # Set to empty string for default.
#         'CONN_MAX_AGE': 600,  # number of seconds database connections should persist for
#     }
# }
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'mysite',
#         'USER': 'waskleani',
#         'PASSWORD': 'postgrespwd',
#         'HOST': 'localhost',  # Set to empty string for localhost.
#         'PORT': '5432',  # Set to empty string for default.
#         'CONN_MAX_AGE': 600,  # number of seconds database connections should persist for
#     }
# }
