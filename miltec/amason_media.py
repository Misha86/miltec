# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

from decouple import config


AWS_S3_SECURE_URLS = False
AWS_QUERYSTRING_AUTH = False
AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = 'miltec'
AWS_S3_HOST = "s3-us-west-2.amazonaws.com"

MEDIAFILES_LOCATION = 'media'

DEFAULT_FILE_STORAGE = 'miltec.custom_storages.MediaStorage'

COMPRESS_STORAGE = DEFAULT_FILE_STORAGE
COMPRESS_URL = 'http://{}.{}'.format(AWS_STORAGE_BUCKET_NAME, AWS_S3_HOST)


