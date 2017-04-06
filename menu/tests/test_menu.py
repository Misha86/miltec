# -*- encoding: utf-8 -*-
"""This module for testing hello app."""

from __future__ import unicode_literals

from django.core.urlresolvers import resolve
from django.test import (TestCase, Client)
from django.template.loader import render_to_string
from django.utils.text import slugify

from ..views import (homepage, shop)
from ..models import (Category, Item)


class MenuTests(TestCase):
    """
    This class for testing a menu app .
    """

    def setUp(self):
        """
        Every test needs a client
        """
        self.client = Client()
        self.category = Category(title='Одежда', used=True)
        self.category.save()

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
        Check menu model and
        Category`s string representation
        """
        self.assertEqual(self.category.title, 'Одежда')
        self.assertTrue(self.category.used)
        self.assertEqual(str(self.category), self.category.title)

        self.assertEqual(self.category.slug, slugify(self.category.title, allow_unicode=True))

    def test_item_model(self):
        """
        Check item model and
        Items`s string representation
        """
        item = Item(title='Плащ', content_type=self.category.get_content_type(), object_id=1)

        self.assertEqual(item.title, 'Плащ')
        self.assertEqual(str(item), item.title)
        item.save()

        self.assertEqual(item.slug, "{}-{}".format(slugify(item.title, allow_unicode=True),
                                                   item.object_id))
        self.assertIsNone(item.parent)
        self.assertFalse(item.children())
        self.assertFalse(item.has_parent_children())

        filter_by_instance = Item.objects.filter_by_instance(instance=item)

        self.assertFalse(filter_by_instance)