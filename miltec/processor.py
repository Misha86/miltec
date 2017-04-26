# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

from buyer.forms import BuyerLoginForm
import requests
from bs4 import BeautifulSoup
from decimal import Decimal


def login_form(request):
    return {'login_form': BuyerLoginForm}


def exchange_rates(request):

    url = 'https://old.kurs.com.ua/informer/inf2'

    try:
        url_requests = requests.get(url).content

        soup_data = BeautifulSoup(url_requests, "html.parser")

        exchange_soup = soup_data.find_all('div', attrs={'class': 'with-arrows'}, limit=6)[-1]

        print(exchange_soup)

        exchange = Decimal(exchange_soup.next_element).quantize(Decimal("0.00"))
    except Exception as ex:
        exchange = False

    return {'exchange': exchange}
