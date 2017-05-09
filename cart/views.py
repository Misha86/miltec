from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from product.models import Product
from .cart import Cart
from django.core.urlresolvers import reverse
from django.http import JsonResponse
from django.template.loader import render_to_string
from cart.forms import BuyerOrderingForm


@require_POST
def cart_add(request, product_id):
    if request.is_ajax():
        data = dict()
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        form = product.get_cart_form(request_form=request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            cart.add(product=product, quantity=cd['quantity'],
                     size=cd['size'], update_quantity=cd['update'])

            data['form_valid'] = True
            data['total_price'] = cart.get_total_price()
        else:
            data['form_valid'] = False
        return JsonResponse(data)
    else:
        return redirect(reverse('menu:shop'))


def cart_remove(request, product_id, size):
    if request.is_ajax():
        data = dict()
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        cart.remove(product, size)

        data['total_price'] = cart.get_total_price()
        if not cart.get_total_price():
            data['empty_cart'] = render_to_string('empty_cart.html', request=request)
        return JsonResponse(data)

    return redirect('cart:detail')


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart_detail.html', {'cart': cart})


def ordering(request):
    cart = Cart(request)
    if cart:
        if request.user.is_authenticated():
            form = BuyerOrderingForm(initial={'email': request.user.email,
                                              'first_name': request.user.first_name,
                                              'last_name': request.user.last_name,
                                              'phone_number': request.user.phone_number})
        else:
            form = BuyerOrderingForm()
        if request.POST:
            form = BuyerOrderingForm(request.POST)
            if form.is_valid():
                return redirect('cart:detail')

        context = {'form': form,
                   'cart': cart}

        return render(request, 'cart_ordering.html', context)
    else:
        return redirect('menu:shop')