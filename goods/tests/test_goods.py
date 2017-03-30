# -*- encoding: utf-8 -*-
"""This module for testing hello app."""

from __future__ import unicode_literals

from django.core.urlresolvers import resolve
from django.test import (TestCase, Client)


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

    def test_shop_page(self):
        """
        Test shop page view
        """
        # Issue a GET request.
        response = self.client.get('/shop/')

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)