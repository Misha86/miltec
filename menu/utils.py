# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

from django.utils.http import is_safe_url, urlunquote
from django.core.mail import mail_admins
from ipware.ip import get_ip
from django.contrib.gis.geoip2 import GeoIP2


def bootstrap_query(array, num):
    new_list = []
    length = int(len(array)//num)
    rest = len(array) % num
    b = 0
    for i in range(length):
        new_list.append(array[b:b+num])
        b += num
    if rest:
        new_list.append(array[len(array)-rest:])
    return new_list


def send_details_user(request):
    ip = get_ip(request)

    user_ip = request.session.get('user_ip', False)

    if not user_ip or user_ip != ip:
        if ip is not None:
            g = GeoIP2()
            try:
                location = g.city(ip)
            except:
                location = {'Локация': 'нет данных'}

        if request.user.is_authenticated():
            subject = "Пользователь: {}".format(request.user.get_full_name())
        else:
            subject = "Пользователь: {}".format(request.user)

        message = "{0};\n IP: {1};\n Регіон: {2};\n " \
                  "Город: {8};\n Страна: {3};\n Код страны: {4};\n " \
                  "Долгота: {5};\n Шырота: {6};\n " \
                  "Почтовый код: {7}.".format(subject,
                                              ip,
                                              location.get('region', None),
                                              location.get('country_name', None),
                                              location.get('country_code', None),
                                              location.get('longitude', None),
                                              location.get('latitude', None),
                                              location.get('postal_code', None),
                                              location.get('city', None),)
        mail_admins(subject, message)
        request.session.set_expiry(0)
        request.session['user_ip'] = ip


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_next_url(request):
    next = request.META.get('HTTP_REFERER')
    if next:
        next = urlunquote(next)  # HTTP_REFERER may be encoded.
    if not is_safe_url(url=next, host=request.get_host()):
        next = '/'
    return next
