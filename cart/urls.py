# -*- coding: UTF-8 -*-
from __future__ import unicode_literals


from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.cart_detail, name='detail'),
    url(r'^remove/(?P<product_id>\d+)/(?P<size>.*)/$', views.cart_remove, name='remove'),
    url(r'^add/(?P<product_id>\d+)/$', views.cart_add, name='add'),
]
