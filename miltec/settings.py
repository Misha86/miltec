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

# SMTP backend(default) for send email

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = 'smtp.gmail.com'                    # Имя хоста используемое для отправки электронных писем. По умолчанию 'localhost'
EMAIL_HOST_USER = config('EMAIL_HOST_USER')     # Имя пользователя используемое при подключении к SMTP серверу указанному в EMAIL_HOST
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')                 # Пароль для подключения к SMTP сервера, который указан в EMAIL_HOST
EMAIL_SUBJECT_PREFIX = '[Django]'              # Префикс добавляемый к теме электронного письма
EMAIL_PORT = 587                               # Порт, используемый при подключении к SMTP серверу указанному в EMAIL_HOST 2525.
EMAIL_USE_TLS = True                         # Указывает использовать ли TLS (защищенное) соединение с SMTP сервером. По умолчанию использует 587 порт .
#EMAIL_USE_SSL = True                          # Указывает использовать ли TLS (защищенное) соединение с SMTP сервером. По умолчанию использует 465 порт.

DEFAULT_FROM_EMAIL = 'mishaelitzem2@rambler.ru'

# Настройка предусматривает отправку разработчикам сайта
#  сообщений обо всех необработанных исключениях по электронной почте
ADMINS = [
    ("Михайло Поліщук", "mishaelitzem2@rambler.ru"),
    ]

# Кортеж по формату аналогичен ADMINS, который определяет кто получает оповещение о “сломанных” ссылках
MANAGERS = ADMINS

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
    'buyer.apps.BuyerConfig'
]


if not DEBUG:
    from .amason_media import *
    INSTALLED_APPS.append('storages')


MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
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
                 os.path.join(BASE_DIR, 'buyer', 'templates', 'buyer')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # my processors
                'miltec.processor.login_form',
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

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
    os.path.join(BASE_DIR, 'menu', 'static', 'menu'),
    os.path.join(BASE_DIR, 'product', 'static', 'product'),
    os.path.join(BASE_DIR, 'buyer', 'static', 'buyer'),
)

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# MEDIA_URL = '/media/'
MEDIA_URL = 'http://www.miltec-sturm.de/'
#
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media_root')

FIXTURE_DIRS = [
    os.path.join(BASE_DIR, 'menu', 'fixtures', 'menu'),
    os.path.join(BASE_DIR, 'product', 'fixtures', 'product'),
    os.path.join(BASE_DIR, 'buyer', 'fixtures', 'buyer'),
    os.path.join(BASE_DIR, 'fixtures', 'auth')
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
