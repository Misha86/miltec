# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

from django.shortcuts import (render, redirect)
from .models import Category
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string
from django.http import JsonResponse, HttpResponse

from .utils import (bootstrap_query, send_details_user)


def homepage(request):
    response = HttpResponse(render(request, "base.html"))
    new_response = send_details_user(request, response)
    return new_response


def shop(request):
    categories_all = Category.objects.all()
    categories = categories_all.filter(promotions=False)
    categories_list = bootstrap_query(categories, 2)
    context = {'category_title': 'ТОВАРЫ',
               'menu_list': categories_list,
               'categories': categories,
               'promotions': categories_all.filter(promotions=True)}

    return render(request, "shop.html", context)


def items_list(request, slug=None):

    if request.is_ajax():
        data = dict()
        category = get_object_or_404(Category, slug=slug)
        items = category.items.all()
        if items.exists():
            items_bootstrap = bootstrap_query(items, 2)
            context = {
                'category_title': category.title,
                'menu_list': items_bootstrap,
                }
            data['html_items'] = render_to_string('partial_shop_main.html',
                                                  context,
                                                  request=request)
            data['is_data'] = True

        else:
            data['ia_data'] = False

        return JsonResponse(data)

    else:
        return redirect(reverse('menu:shop'))






