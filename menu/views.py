from django.shortcuts import (render, redirect)
from .models import Category
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string
from django.http import JsonResponse



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


def homepage(request):
    return render(request, "base.html")


def shop(request):
    categories_all = Category.objects.all()
    categories = categories_all.filter(promotions=False)
    categories_list = bootstrap_query(categories, 2)
    context = {
        'category_title': 'ТОВАРЫ',
        'menu_list': categories_list,
        'categories': categories,
        'promotions': categories_all.filter(promotions=True)
    }
    return render(request, "shop.html", context)


def items_list(request, slug=None):

    if request.is_ajax():
        data = dict()
        category = get_object_or_404(Category, slug=slug)
        items = category.items.all()
        if items.exists():
            items_list = bootstrap_query(items, 2)
            context = {
                'category_title': category.title,
                'menu_list': items_list,
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






