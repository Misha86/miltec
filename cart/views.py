from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from product.models import Product
from .cart import Cart
from .forms import CartAddProductForm
from django.core.urlresolvers import reverse
from django.http import JsonResponse


@require_POST
def cart_add(request, product_id):
    if request.is_ajax():
        data = dict()
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        form = CartAddProductForm(request.POST)
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
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product, size)
    return redirect('cart:detail')


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart_detail.html', {'cart': cart})