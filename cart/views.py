# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from product.models import Product
from .cart import Cart
from django.core.urlresolvers import reverse
from django.http import JsonResponse
from django.template.loader import render_to_string
from cart.forms import SendMassageForm
from django.conf import settings
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.contrib import messages


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
            massage_form = SendMassageForm(initial={'cart_email': request.user.email,
                                                    'first_name': request.user.first_name,
                                                    'last_name': request.user.last_name,
                                                    'phone_number': request.user.phone_number})
        else:
            massage_form = SendMassageForm()

        if request.POST:
            massage_form = SendMassageForm(request.POST)
            if massage_form.is_valid():
                cart_email = massage_form.cleaned_data['cart_email']
                first_name = massage_form.cleaned_data['first_name']
                last_name = massage_form.cleaned_data['last_name']
                phone_number = massage_form.cleaned_data['phone_number']
                address = massage_form.cleaned_data['address']

                html_content = '<p>This is an <strong>important</strong> message.</p>'

                subject = "{} {}".format(first_name.title(), last_name.title())
                massage = "E-mail: {};\nPhone number: {}\nPost address: {}".format(cart_email, phone_number, address)
                from_email = settings.EMAIL_HOST_USER
                to_email = [settings.EMAIL_HOST_USER, 'mishaelitzem2@rambler.ru']
                # send_mail(subject, massage, from_email, to_email, html_message=html_content, fail_silently=False)

                msg = EmailMultiAlternatives(subject, massage, from_email, to_email)
                msg.attach_alternative(html_content, "text/html")
                # msg.send()

                messages.success(request, 'Заказ офомлен успешно. Ждите нашего дзвонка!', extra_tags='success')
                return redirect('menu:homepage')

        context = {'form': massage_form,
                   'cart': cart}

        return render(request, 'cart_ordering.html', context)
    else:
        return redirect('menu:shop')




