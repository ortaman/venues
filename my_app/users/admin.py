
from django.contrib import admin
from .models import User


class UserAdmin(admin.ModelAdmin):

    list_display = ('email', 'username', 'names', 'surnames')
    list_filter = ('is_staff', 'is_active')

    fieldsets = (
        ('Autenticación',
            {'fields': ('email', 'username', 'password')}),
        ('Información personal',
            {'fields': ('names', 'surnames', 'gender', 'phone',)}),
        ('Información adicional',
            {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups')}),
        ('Información adicional',
            {'fields': ('created_at', 'updated_at')}),
    )

    readonly_fields = ('created_at', 'updated_at')

    search_fields = ('email', 'surnames',)
    ordering = ('surnames', 'email')
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
