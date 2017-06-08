# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views


urlpatterns = [
    url(r'^password_reset/$', auth_views.password_reset, {'template_name': 'password_reset_form.html',
                                                          'email_template_name': 'password_reset_email.html',
                                                          'html_email_template_name': 'password_reset_email.html',
                                                          'subject_template_name': 'password_reset_subject.txt',
                                                          'post_reset_redirect': 'buyer:password_reset_done'},
        name='password_reset'),
    url(r'^password_reset/done/$', auth_views.password_reset_done, {'template_name': 'password_reset_done.html',
                                                                    'current_app': 'buyer'},
        name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm,
        {'template_name': 'password_reset_confirm.html',
         'post_reset_redirect': 'buyer:password_reset_complete'},
        name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete,
        {'template_name': 'password_reset_complete.html'},
        name='password_reset_complete'),

    url(r'^login/$', views.login, name='login'),
    url(r'^register/$', views.register, name='register'),
    url(r'^update/$', views.update, name='update'),
    url(r'^delete/(?P<id>[0-9]+)/$', views.delete, name='delete'),
    url(r'^logout/$', views.logout, name='logout'),
    ]

