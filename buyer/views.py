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

from .forms import (BuyerLoginForm, BuyerRegisterForm)


User = get_user_model()


def update(request):
    path = request.META.get('HTTP_REFERER', '/')
    if path == request.build_absolute_uri():
        return_path = '/'
    else:
        return_path = path
    instance = get_object_or_404(User, username=request.user)
    form = ProfileUpdateForm(request.POST or None, request.FILES or None, instance=instance,
                             initial={'date_of_birth': instance.profile.date_of_birth,
                                      'sex': instance.profile.sex,
                                      'avatar': instance.profile.avatar})
    if form.is_valid():
        form.save()
        profile = instance.profile
        profile.date_of_birth = form.cleaned_data['date_of_birth']
        profile.sex = form.cleaned_data['sex']
        profile.avatar = form.cleaned_data['avatar']
        profile.save()
        update_session_auth_hash(request, form.instance)
        messages.success(request, _('Ви змінили свій профіль, ' + instance.username + '!'),
                         extra_tags='success')
        return redirect(return_path)
    else:
        form = form
    title = _('Форма для зміни профіля \'' + str(instance.get_full_name() + '\''))
    button_update = _('Змінити')
    button_delete = _('Видалити')
    context = {
        'title': title,
        'button_create': button_update,
        'button_delete': button_delete,
        'form': form,
        'return_path': return_path,
        'profile': instance,
        }
    return render(request, 'register.html', context)


def delete(request, id=None):
    instance = get_object_or_404(User, id=id)
    name = instance.get_full_name()
    return_path = settings.LOGIN_REDIRECT_URL
    title = _('Ви впевнені, що хочете видалити профіль \'' + name + '\' ?')
    button_delete = _('видалити профіль')
    button_cancel = _('відміна')
    context = {
        'title': title,
        'button_delete': button_delete,
        'button_cancel': button_cancel,
        'return_path': return_path,
        }
    if request.POST:
        instance.delete()
        messages.success(request, _('Користувач \'' + name + '\' видалений!'), extra_tags='success')
        return redirect(return_path)
    return render(request, 'profile_delete_form.html', context)


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

    context = {
        'form': form,
    }
    return render(request, 'register.html', context)



