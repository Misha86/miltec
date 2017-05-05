from django.shortcuts import redirect, render, get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.contrib import auth
from django.core.context_processors import csrf
from .models import BuyerUser
# from .forms import (ProfileCreationForm,
#                            ProfileUpdateForm)
from django.contrib import messages
from django.conf import settings
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.core.urlresolvers import reverse
from django.conf import settings

from .forms import (BuyerLoginForm, BuyerRegisterForm, BuyerUpdateForm)


User = get_user_model()


def login(request):

    if request.is_ajax() and request.method == 'POST':
        data = dict()
        form = BuyerLoginForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = auth.authenticate(username=email, password=password)

            if user is not None and user.is_active:
                del request.session[settings.CART_SESSION_ID]
                auth.login(request, user)
                data['form_valid'] = True
                path = request.GET.get('next')

                if path != reverse('buyer:login'):
                    redirect_path = path
                else:
                    redirect_path = '/'

                data['redirect_path'] = redirect_path

        data['form_html'] = render_to_string('login.html', {'login_form': form}, request=request)

        return JsonResponse(data)

    return redirect('/')


def logout(request):
    # messages.success(request, 'Щастливо, ' + request.user.username + '!', extra_tags='success')
    auth.logout(request)
    path = request.GET.get('next', '')
    if path:
        return redirect(path)
    else:
        return redirect(reverse('menu:homepage'))


def register(request):

    form = BuyerRegisterForm()
    if request.POST:
        form = BuyerRegisterForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password2']
            buyer = BuyerUser(email=form.cleaned_data['email'], first_name=form.cleaned_data['first_name'],
                              last_name=form.cleaned_data['last_name'],
                              date_of_birth=form.cleaned_data['date_of_birth'],
                              sex=form.cleaned_data['sex'],
                              phone_number=form.cleaned_data['phone_number'],
                              address=form.cleaned_data['address'])
            buyer.set_password(password)
            buyer.save()

            new_buyer = auth.authenticate(username=buyer.email, password=password)

            auth.login(request, new_buyer)
            # messages.success(request, 'Дякую, що долучилися до нас, ' + new_profile.user.username + '!',
            #                  extra_tags='success')
            return redirect(reverse('menu:homepage'))
        else:
            form = form

    title = "Форма регистрации"
    button_create = 'РЕГИСТРИРОВАТЬСЯ'

    context = {
        'title': title,
        'button_create': button_create,
        'form': form,
        }
    return render(request, 'register.html', context)


def update(request):
    instance = get_object_or_404(User, email=request.user)
    form = BuyerUpdateForm(request.POST or None, instance=instance,
                           initial={'address': instance.address})
    if form.is_valid():
        form.save()
        update_session_auth_hash(request, form.instance)
        # messages.success(request, _('Ви змінили свій профіль, ' + instance.username + '!'),
        #                  extra_tags='success')
        return redirect(reverse('menu:homepage'))
    else:
        form = form
    title = "Форма для изменения профиля '{}'".format(instance.get_full_name())
    button_update = 'ИЗМЕНИТЬ'
    button_delete = 'УДАЛИТЬ'
    context = {
        'title': title,
        'button_create': button_update,
        'button_delete': button_delete,
        'form': form,
        'profile': instance,
        }
    return render(request, 'register.html', context)


def delete(request, id=None):
    if request.is_ajax():
        data = dict()
        instance = get_object_or_404(User, id=id)
        title = "Вы уверены, что хотите удалить свой профиль '{}'?".format(instance.get_full_name())
        button_delete = 'УДАЛИТЬ ПРОФИЛЬ'
        button_cancel = 'ОТМЕНА'
        context = {
            'title': title,
            'button_delete': button_delete,
            'button_cancel': button_cancel
            }

        data['delete_form'] = render_to_string('delete_form.html', context, request=request)

        if request.POST:
            instance.delete()
            data['is_data'] = True
            data['redirect_path'] = reverse('menu:homepage')
            # messages.success(request, _('Користувач \'' + name + '\' видалений!'), extra_tags='success')

        return JsonResponse(data)

    return redirect(reverse('menu:homepage'))
