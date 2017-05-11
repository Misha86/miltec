# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
from decouple import config


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


