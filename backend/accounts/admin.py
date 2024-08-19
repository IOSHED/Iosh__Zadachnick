from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    list_display = (
        'email', 'name', 'surname', 'birthday_at', 'is_active', 'is_staff', 'is_superuser', 'is_email_verification',
        'chat_id',
    )
    search_fields = ('email', 'name', 'surname')
    ordering = ('email',)
    filter_horizontal = ()
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'is_email_verification')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('name', 'surname', 'birthday_at')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_email_verification')}),
        ('Icons', {'fields': ('icon32', 'icon64')}),
        ('Important dates', {'fields': ('last_login', 'create_at', 'update_at')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'surname', 'birthday_at', 'password1', 'password2'),
        }),
    )
    readonly_fields = ('create_at', 'update_at')


admin.site.register(CustomUser, CustomUserAdmin)
