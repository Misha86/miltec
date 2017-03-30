# -*- encoding: utf-8 -*-
"""This module for testing hello app."""

from __future__ import unicode_literals

from django.core.urlresolvers import resolve
from django.test import (TestCase, Client)
from django.template.loader import render_to_string

from ..views import (homepage, shop)
from ..models import Category


class GoodsTests(TestCase):
    """
    This class for testing a goods app .
    """

    def setUp(self):
        """
        Every test needs a client
        """
        self.client = Client()

    def test_homepage(self):
        """
        Test homepage view
        """
        # Issue a GET request.
        response = self.client.get('/')

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        with self.assertTemplateUsed(template_name='base.html'):
            render_to_string('base.html')

    def test_shop_page(self):
        """
        Test shop page view
        """
        # Issue a GET request.
        response = self.client.get('/shop/')

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        with self.assertTemplateUsed(template_name='shop.html'):
            render_to_string('shop.html')

    def test_url_resolves_homepage_view(self):
        """
        Check homepage view by url
        """
        found = resolve('/')
        self.assertEqual(found.func, homepage)
        self.assertEqual(found.url_name, 'homepage')

    def test_url_resolves_shop_view(self):
        """
        Check shop view by url
        """
        found = resolve('/shop/')
        self.assertEqual(found.func, shop)
        self.assertEqual(found.url_name, 'shop')

    def test_category_model(self):
        """
        Check category model and
        Category`s string representation
        """
        category = Category(title='Одежда', state=True)

        self.assertEqual(category.id, 1)
        self.assertEqual(category.title, 'Одежда')
        self.assertTrue(category.state)

        self.assertEqual(str(category), category.title)