# -*- coding: UTF-8 -*-
from __future__ import unicode_literals


# $ heroku addons:create memcachier:dev  - it`s not free
def get_cache():
    import os
    try:
        os.environ['MEMCACHE_SERVERS'] = os.environ['MEMCACHIER_SERVERS'].replace(',', ';')
        os.environ['MEMCACHE_USERNAME'] = os.environ['MEMCACHIER_USERNAME']
        os.environ['MEMCACHE_PASSWORD'] = os.environ['MEMCACHIER_PASSWORD']
        return {
            'default': {
                'BACKEND': 'django_pylibmc.memcached.PyLibMCCache',
                'TIMEOUT': 500,
                'BINARY': True,
                'OPTIONS': {'tcp_nodelay': True}
            }
        }
    except:
        return {
            'default': {
                # 'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'    for heroku local cache
                # 'BACKEND': 'django.core.cache.backends.memcached.PyLibMCCache', for django-pylibmc
                'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache', # for python-memcached
                'KEY_PREFIX': 'miltec',
                'TIMEOUT': 86400,
                'LOCATION': '127.0.0.1:11211',
                'OPTIONS': {
                    'MAX_ENTRIES': 500,
                    'CULL_FREQUENCY': 2,
                    }
            }
        }


CACHES = get_cache()

