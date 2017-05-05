# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

from django.conf.urls import include, url
from . import views


urlpatterns = [
    url(r'^login/$', views.login, name='login'),
    url(r'^register/$', views.register, name='register'),
    url(r'^update/$', views.update, name='update'),
    url(r'^delete/(?P<id>[0-9]+)/$', views.delete, name='delete'),
    url(r'^logout/$', views.logout, name='logout'),
]

