from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from users.models import User, _
from django.contrib import admin


@admin.register(User)
class UserAdmin(DjangoUserAdmin):

    fieldsets = (
        (None, {'fields': ('telegram_id', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'avatar')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('telegram_id', 'password1', 'password2'),
        }),
    )
    list_display = ('telegram_id', 'is_staff')
    search_fields = ('telegram_id', 'first_name', 'last_name')
    ordering = ('telegram_id', )
