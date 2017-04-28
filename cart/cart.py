# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

from decimal import Decimal
from django.conf import settings
from product.models import Product


# class Cart(object):
#     def __init__(self, request):
#         # Инициализация корзины пользователя
#         self.user = request.user.is_authenticated()
#         self.session = request.session
#         cart = self.session.get(settings.CART_SESSION_ID)
#         if not cart:
#             # Сохраняем корзину пользователя в сессию
#             cart = self.session[settings.CART_SESSION_ID] = {}
#         self.cart = cart
#
#     # Добавление товара в корзину пользователя или обновление количества товара
#     def add(self, product, quantity=1, update_quantity=False):
#         product_id = str(product.id)
#         if product_id not in self.cart:
#             if self.user:
#                 price = product.price_for_users
#             else:
#                 price = product.price
#             self.cart[product_id] = {'quantity': 0,
#                                      'price': str(price)}
#         if update_quantity:
#             self.cart[product_id]['quantity'] = quantity
#         else:
#             self.cart[product_id]['quantity'] += quantity
#         self.save()
#
#     # Сохранение данных в сессию
#     def save(self):
#         self.session[settings.CART_SESSION_ID] = self.cart
#         # Указываем, что сессия изменена
#         self.session.modified = True
#
#     def remove(self, product):
#         product_id = str(product.id)
#         if product_id in self.cart:
#             del self.cart[product_id]
#             self.save()
#
#     # Итерация по товарам
#     def __iter__(self):
#         product_ids = self.cart.keys()
#         products = Product.objects.filter(id__in=product_ids)
#         for product in products:
#             self.cart[str(product.id)]['product'] = product
#
#         for item in self.cart.values():
#             item['price'] = Decimal(item['price'])
#             item['total_price'] = item['price'] * item['quantity']
#             yield item
#
#     # Количество товаров
#     def __len__(self):
#         return sum(item['quantity'] for item in self.cart.values())
#
#     def get_total_price(self):
#         return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())
#
#     def clear(self):
#         del self.session[settings.CART_SESSION_ID]
#         self.session.modified = True


class Cart(object):
    def __init__(self, request):
        # Инициализация корзины пользователя
        self.user = request.user.is_authenticated()
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # Сохраняем корзину пользователя в сессию
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    # Добавление товара в корзину пользователя или обновление количества товара
    def add(self, product, quantity=1, size=None, update_quantity=False):
        product_id = str(product.id)
        product_size = str(size)

        if self.user:
            price = product.price_for_users
        else:
            price = product.price

        if product_id not in self.cart:
            self.cart[product_id] = {product_size: {'quantity': 0,
                                                    'size': product_size,
                                                    'price': str(price)}}

        elif product_id in self.cart and product_size not in self.cart[product_id].keys():
            self.cart[product_id].update({product_size: {'quantity': 0,
                                                         'size': product_size,
                                                         'price': str(price)}})

        if update_quantity:
            self.cart[product_id][product_size]['quantity'] = quantity
        else:
            self.cart[product_id][product_size]['quantity'] += quantity
        self.save()

    # Сохранение данных в сессию
    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        # Указываем, что сессия изменена
        self.session.modified = True

    def remove(self, product, size=None):
        product_id = str(product.id)
        product_size = str(size)
        if product_id in self.cart:
            del self.cart[product_id][product_size]
            self.save()

    # Итерация по товарам
    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            size_item = self.cart[str(product.id)].keys()
            for size in size_item:
                self.cart[str(product.id)][size]['product'] = product

            for item in self.cart[str(product.id)].values():
                item['price'] = Decimal(item['price'])
                item['total_price'] = item['price'] * item['quantity']
                yield item

    # Количество товаров
    def __len__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        count_products = []
        for product in products:
            for item in self.cart[str(product.id)].values():
                count_products.append(item['quantity'])
        return sum(count_products)

    def get_total_price(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        count_products = []
        for product in products:
            for item in self.cart[str(product.id)].values():
                res = Decimal(item['price']) * item['quantity']
                count_products.append(res)
        return sum(count_products)

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True