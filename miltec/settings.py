"""
Django settings for miltec project.

Generated by 'django-admin startproject' using Django 1.9.6.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os
from django.contrib.messages import constants as message_constants
from decouple import config, Csv
import dj_database_url
from .send_mail_settings import *
# from .memcached_cache import *


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())

SITE_ID = 1

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # other apps
    'phonenumber_field',
    'address',
    # my apps
    'menu.apps.MenuConfig',
    'product.apps.ProductConfig',
    'buyer.apps.BuyerConfig',
    'cart.apps.CartConfig'
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # 'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.cache.FetchFromCacheMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]

ROOT_URLCONF = 'miltec.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'),
                 os.path.join(BASE_DIR, 'menu', 'templates', 'menu'),
                 os.path.join(BASE_DIR, 'product', 'templates', 'product'),
                 os.path.join(BASE_DIR, 'buyer', 'templates', 'buyer'),
                 os.path.join(BASE_DIR, 'buyer', 'templates', 'registration'),
                 os.path.join(BASE_DIR, 'cart', 'templates', 'cart')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # my processors
                'miltec.processor.login_form',
                'miltec.processor.cart',
                'miltec.processor.exchange_rates'
                ],
            },
        },
    ]

WSGI_APPLICATION = 'miltec.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {}
}

db_from_env = dj_database_url.config(conn_max_age=500)
if db_from_env:
    DATABASES['default'].update(db_from_env)
else:
    DATABASES['default'].update({
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        })

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Europe/Kiev'

USE_I18N = True

USE_L10N = False

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

MESSAGE_LEVEL = message_constants.DEBUG

# Support for X-Request-ID

LOG_REQUEST_ID_HEADER = 'HTTP_X_REQUEST_ID'

LOG_REQUESTS = True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'request_id': {
            '()': 'log_request_id.filters.RequestIDFilter'
        }
    },
    'formatters': {
        'standard': {
            'format': '%(levelname)-8s [%(asctime)s] [%(request_id)s] %(name)s: %(message)s'
        },
        },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'filters': ['request_id'],
            'formatter': 'standard',
            },
        },
    'loggers': {
        'log_request_id.middleware': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
            },
        }
}

# отключить отчёты о 404 ошибке URL страницы заканчивается
import re
IGNORABLE_404_URLS = (
    re.compile(r'^/apple-touch-icon.*\.png$'),
    re.compile(r'^/favicon\.ico$'),
    re.compile(r'^/robots\.txt$'),
)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

if not DEBUG:
    from .amason_media import *
    INSTALLED_APPS.append('storages')

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
    os.path.join(BASE_DIR, 'menu', 'static', 'menu'),
    os.path.join(BASE_DIR, 'product', 'static', 'product'),
    os.path.join(BASE_DIR, 'buyer', 'static', 'buyer'),
    os.path.join(BASE_DIR, 'address', 'static', 'address'),
    os.path.join(BASE_DIR, 'cart', 'static', 'cart'),
)

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = config('MEDIA_URL', default='/media/')
# MEDIA_URL = 'http://www.miltec-sturm.de/'


MEDIA_ROOT = os.path.join(BASE_DIR, 'media_root')

FIXTURE_DIRS = [
    os.path.join(BASE_DIR, 'menu', 'fixtures', 'menu'),
    os.path.join(BASE_DIR, 'product', 'fixtures', 'product'),
    os.path.join(BASE_DIR, 'buyer', 'fixtures', 'buyer'),
    os.path.join(BASE_DIR, 'address', 'fixtures', 'address')
    ]


AUTH_USER_MODEL = 'buyer.BuyerUser'


PHONE_NUMBER_REGION = 'UK'
PHONE_NUMBERS_FORMATS_BY_REGION = {
    'UK': {
        'pattern': '(\\d{12})', 'format': '\\12', 'prefix_format': '+%s (%s)'
    },
    'US': {
        'pattern': '(\\d{3})(\\d{3})(\\d{4})', 'format': '\\1 \\2-\\3', 'prefix_format': '+%s (%s)'
    },
}

# cart
CART_SESSION_ID = 'cart'

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'


GEOIP_PATH = os.path.join(BASE_DIR, 'miltec', 'geo')

LOGIN_URL = 'buyer:login'