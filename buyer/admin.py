from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from buyer.models import BuyerUser
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.password_validation import validate_password

from address.forms import AddressField, AddressWidget


class BuyerCreationForm(forms.ModelForm):
    """A form for creating new_profile users. Includes all the required
    fields, plus a repeated password."""
    address = AddressField(label='Адрес', widget=AddressWidget(attrs={'placeholder': 'введите свой адрес'}),
                           help_text='улица Макарова, 24, Ровно, Ровенская область, Украина')

    password1 = forms.CharField(label=_('Password'),
                                widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                  'placeholder': _('введите пароль')}))
    password2 = forms.CharField(label=_('Password confirmation'),
                                widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                  'placeholder': _('повторите пароль')}))

    class Meta:
        model = BuyerUser
        fields = ('email', 'first_name', 'last_name', 'date_of_birth', 'sex', 'phone_number')

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        valid_password = validate_password(password1)
        if valid_password is not None:
            raise valid_password.ValidationError()
        return password1

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Пароли не совпадают")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(BuyerCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class BuyerChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()
    address = AddressField()

    class Meta:
        model = BuyerUser
        fields = ('email', 'password', 'first_name', 'last_name', 'date_of_birth', 'sex', 'phone_number',
                  'sex', 'is_active', 'is_admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class BuyerAdmin(BaseUserAdmin):
    # The forms to add and change user instancesn@r.ru
    form = BuyerChangeForm
    add_form = BuyerCreationForm
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'get_full_name', 'get_sex', 'date_of_birth', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('date_of_birth', 'sex', 'first_name', 'last_name', 'phone_number', 'address')}),
        ('Permissions', {'fields': ('is_admin', 'is_active')}),
        ('Important dates', {'fields': ('last_login', )})
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'date_of_birth', 'sex', 'first_name', 'last_name',
                       'phone_number', 'address', 'password1', 'password2')}),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

# Now register the new_profile UserAdmin...
admin.site.register(BuyerUser, BuyerAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)
