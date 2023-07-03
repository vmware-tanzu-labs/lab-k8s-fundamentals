import os

"""
Django settings for frontend project.

Generated by 'django-admin startproject' using Django 1.10.6.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os
import json

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# If persistent volume mounted, use it for database and media.
if os.path.isdir('/opt/app-root/data'):
    DATA_DIR = '/opt/app-root/data'
else:
    DATA_DIR = os.path.join(BASE_DIR, 'data')

if os.path.isdir('/opt/app-root/media'):
    MEDIA_DIR = '/opt/app-root/media'
else:
    MEDIA_DIR = os.path.join(DATA_DIR, 'media')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'w9mp-ntfm6b1k1!i3nx6kd)jehhnu=r)o)0d!s*rn&36dtquth'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'mod_wsgi.server',
    'blog',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'frontend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'blog.context_processors.site_information'
            ],
        },
    },
]

WSGI_APPLICATION = 'frontend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

import dj_database_url

if os.path.isdir('/opt/app-root/secrets/database'):
    def database_url():
        try:
            from urllib.parse import urlparse
        except ImportError:
            from urlparse import urlparse

        with open('/opt/app-root/secrets/database/database_name') as fp:
            database_name = fp.read().strip()

        with open('/opt/app-root/secrets/database/uri') as fp:
            uri = fp.read().strip()

        with open('/opt/app-root/secrets/database/username') as fp:
            username = fp.read().strip()

        with open('/opt/app-root/secrets/database/password') as fp:
            password = fp.read().strip()

        address = urlparse(uri)

        scheme = address.scheme
        hostname = address.hostname
        port = address.port

        return '%s://%s:%s@%s:%s/%s' % (scheme, username, password,
                hostname, port, database_name)

    DATABASES = {
        'default': dj_database_url.config(default=database_url(),
                conn_max_age=600)
    }

elif os.environ.get('DATABASE_HOST'):
    def database_url():
        scheme = os.environ.get('DATABASE_SCHEME', 'postgres')
        port = os.environ.get('DATABASE_PORT', '5432')
        hostname = os.environ.get('DATABASE_HOST')
        database_name = os.environ.get('DATABASE_NAME')
        username = os.environ.get('DATABASE_USER')
        password = os.environ.get('DATABASE_PASSWORD')

        return '%s://%s:%s@%s:%s/%s' % (scheme, username, password,
                hostname, port, database_name)

    DATABASES = {
        'default': dj_database_url.config(default=database_url(),
                conn_max_age=600)
    }

elif os.environ.get('DATABASE_URL'):
    DATABASES = {
        'default': dj_database_url.config(conn_max_age=600)
    }

else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(DATA_DIR, 'db.sqlite3'),
        }
    }


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = MEDIA_DIR

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
        },
    },
}

LOGIN_REDIRECT_URL = 'post_list'

# Default settings for blog application.

BLOG_SETTINGS = {}
BLOG_SETTINGS_FILE = os.path.join(BASE_DIR, 'settings', 'blog.json')

if os.path.exists(BLOG_SETTINGS_FILE):
    with open(BLOG_SETTINGS_FILE) as fp:
        BLOG_SETTINGS = json.load(fp)

BLOG_SITE_NAME = 'Educates Blog'
BLOG_SITE_NAME = BLOG_SETTINGS.get('BLOG_SITE_NAME', BLOG_SITE_NAME)
BLOG_SITE_NAME = os.environ.get('BLOG_SITE_NAME', BLOG_SITE_NAME)

BLOG_BANNER_COLOR = ''
BLOG_BANNER_COLOR = BLOG_SETTINGS.get('BLOG_BANNER_COLOR', BLOG_BANNER_COLOR)
BLOG_BANNER_COLOR = os.environ.get('BLOG_BANNER_COLOR', BLOG_BANNER_COLOR)

KUBE_POD_NAME = 'localhost'
KUBE_POD_NAME = os.environ.get('HOSTNAME', KUBE_POD_NAME)

# Enable DEBUG mode when mod_wsgi-express debugging enabled.

if os.environ.get('MOD_WSGI_DEBUG_MODE'):
    DEBUG = True

if os.environ.get('MOD_WSGI_DEBUGGER_ENABLED'):
    DEBUG_PROPAGATE_EXCEPTIONS = True
