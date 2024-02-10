from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from import_export.admin import ImportExportModelAdmin

from apps.authentication.models import (
    CustomUser
)


class CustomUserAdmin(ImportExportModelAdmin, UserAdmin):
    model = CustomUser
    list_display = ['email', 'phone', 'is_active', 'is_staff',]
    search_fields = ['email', 'phone', 'groups']
    ordering = ['email']
    fieldsets = (
        (None, {'fields': ('first_name', 'last_name', 'email', 'username', 'phone', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Personal Information', {'fields': ('avatar', )}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'password1', 'password2'),
        }),
    )


admin.site.register(CustomUser, CustomUserAdmin)