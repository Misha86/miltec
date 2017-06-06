# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

from buyer.forms import BuyerLoginForm
from cart.cart import Cart
import requests
from bs4 import BeautifulSoup
from decimal import Decimal
from datetime import (datetime, timedelta)
from django.utils.timezone import make_aware, get_current_timezone


def login_form(request):
    return {'login_form': BuyerLoginForm}


def cart(request):
    response = {}
    cart_response = Cart(request)
    if cart_response:
        response['total_price'] = cart_response.get_total_price()
    return response


def exchange_rates(request):
    if not request.session.get('exchange', False):

        url = 'https://old.kurs.com.ua/informer/inf2'
        try:
            url_requests = requests.get(url).content
            soup_data = BeautifulSoup(url_requests, "html.parser")
            exchange_soup = soup_data.find_all('div', attrs={'class': 'with-arrows'}, limit=6)[-1]
            exchange = Decimal(exchange_soup.next_element).quantize(Decimal("0.00"))
        except Exception as ex:
            exchange = ex

        date_tomorrow = datetime.today() + timedelta(days=1)
        expire_datetime = make_aware(datetime(date_tomorrow.year, date_tomorrow.month, date_tomorrow.day),
                                     get_current_timezone())
        request.session.set_expiry(expire_datetime)
        request.session['exchange'] = exchange

    return {'exchange': request.session['exchange']}
