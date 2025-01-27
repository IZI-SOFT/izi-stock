from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .forms import *


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = (
        'username',
        'email',
        'is_staff',
        'is_admin',
        'is_superuser'

    )
    list_filter = (
        'is_staff',
        'is_superuser',
        'is_active',
        'assigned_branches'
    )
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Assignments', {'fields': ('assigned_branches','assigned_stocks' )}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
            'username', 'password1', 'password2', 'is_staff', 'is_active', 'assigned_stocks', 'assigned_branches'),
        }),
    )

    search_fields = ('username', 'email')
    ordering = ('username',)

