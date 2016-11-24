# -*- coding: utf-8 -*-

from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from django.contrib.auth.forms import (AdminPasswordChangeForm)
from django.utils.translation import ugettext_lazy as _


from core.autenticar.forms import RegistrationForm, UserChangeForm
from core.autenticar.models import User


class MyUserAdmin(UserAdmin):
    # The forms to add and change user instances

    add_form = RegistrationForm
    form = UserChangeForm
    change_password_form = AdminPasswordChangeForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on autenticar.User.
    list_display = ('email','is_superuser','is_active')
    list_filter = ('is_superuser','is_active','groups')
    fieldsets = (
        ('Informações gerais', {'fields': ('email',)}),

        ('Permissions', {'fields': ('is_superuser','is_active','user_permissions','groups')}),
        (_('Datas Importantes'), {'fields': ('last_login', 'date_joined')})
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email','password1', 'password2')}
        ),
    )


    search_fields = ('email',)
    ordering = ('email',)

    filter_horizontal = ('groups', 'user_permissions',)





admin.site.register(User, MyUserAdmin)
