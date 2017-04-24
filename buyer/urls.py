# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

from django.conf.urls import include, url
from . import views


urlpatterns = [
    url(r'^login/$', views.login, name='login'),
    url(r'^register/$', views.register, name='register'),
    url(r'^logout/$', views.logout, name='logout'),
]

