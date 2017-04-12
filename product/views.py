from django.shortcuts import redirect

from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from menu.models import Item
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

from .models import Product


def pagination_products(request, products_all, count_products=2):

    paginator = Paginator(products_all, count_products)
    page = request.GET.get('page')

    try:
        products = paginator.page(page)
        # print(articles.page_range)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        products = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        products = paginator.page(paginator.num_pages)

    return products


def ordering_too(request, products_all, default_ordering='price'):

    # ordering products
    ordering_type = request.GET.get('ordering', '')

    if ordering_type != '' and ordering_type != request.session.get('ordering'):
        request.session['ordering'] = ordering_type
        products = products_all.order_by(ordering_type)
    elif request.session.get('ordering'):
        products = products_all.order_by(request.session.get('ordering'))
    else:
        products = products_all.order_by(default_ordering)

    return products


def view_page(request):
    # views products standard or grid
    view = request.GET.get('view', '')
    if view != '':
        request.session['view'] = view


def product_list(request, slug=None):

    if request.is_ajax():
        data = dict()
        item = get_object_or_404(Item, slug=slug)

        # ordering products
        ordering = request.GET.get('ordering', '')
        if ordering != '' and ordering != request.session.get('ordering'):
            request.session['ordering'] = ordering
            list_product = item.get_all_products(order_by=ordering)
        elif request.session.get('ordering'):
            list_product = item.get_all_products(order_by=request.session.get('ordering'))
        else:
            list_product = item.get_all_products(order_by='price')

        # view products
        view_page(request)

        # pagination products
        products = pagination_products(request, list_product, 2)

        context = {
            'products': products,
            'item': item
        }

        data['html_items'] = render_to_string('product_list.html',
                                              context,
                                              request=request)
        data['is_data'] = True

        return JsonResponse(data)

    else:
        return redirect(reverse('menu:shop'))


def product_details(request, slug=None):

    if request.is_ajax():
        data = dict()
        product = get_object_or_404(Product, slug=slug)

        products = pagination_products(request, product.item.products.all(), 1)

        context = {
            'products': products,
            'product': product,
            'item': product.item
        }

        if products.has_next():
            context['next_slug'] = products.paginator.page(products.next_page_number()).object_list[0].slug

        if products.has_previous():
            context['previous_slug'] = products.paginator.page(products.previous_page_number()).object_list[0].slug

        data['html_items'] = render_to_string('partial_product.html',
                                              context,
                                              request=request)
        data['is_data'] = True

        return JsonResponse(data)

    return redirect(reverse('menu:shop'))


def search(request):
    data = dict()
    products_list = Product.objects.all()

    # search products
    query = request.GET.get('q')
    if request.is_ajax():
        context = {
            'search': True
        }
        if query:
            products_search = products_list.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query)).distinct()

            data['json_query'] = list(products_search.values_list('title', flat=True))

            view_page(request)

            products_ordering = ordering_too(request, products_search)

            products = pagination_products(request, products_ordering, 2)

            if products:

                context.update({
                    'products': products,
                    'item': {
                        'title': 'Searchresult',
                        'returned_title': 'Your Searchrequest » {} « has returned the following.'.format(query)
                    }
                })

            else:
                context.update({
                    'item': {
                        'title': 'Searchresult',
                        'returned_title': 'No results of searching...'
                    }
                })

            data['is_data'] = True

            data['html_items'] = render_to_string('product_list.html',
                                                  context,
                                                  request=request)

        else:

            data['is_data'] = False

        return JsonResponse(data)

    else:

        return redirect(reverse('menu:shop'))


