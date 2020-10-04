from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class CustomUserAdmin(UserAdmin):
    ordering = ('email',)
    list_display = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password', 'first_name',
                           'last_name', 'is_active', 'is_staff',
                           'is_superuser', 'groups')}),
    )
    add_fieldsets = (
        (None, {'fields': ('email', 'password', 'first_name',
                           'last_name', 'is_active', 'is_staff',
                           'is_superuser', 'groups')}),
    )


admin.site.register(User, CustomUserAdmin)
