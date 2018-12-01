
from django.contrib import admin
from .models import Favorite


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'address')
    list_filter = ('added_at',)

    fieldsets = (
        ('Información general',
            {'fields': ('id', 'name', 'address', 'photo', 'lat', 'lng',
                  'tip_count', 'users_count', 'checkins_count', 'visits_count', 'added_by')}),
        ('Información adicional',
            {'fields': ('added_at', 'updated_at')}),
    )

    readonly_fields = ('added_at', 'updated_at')

    search_fields = ('name',)
    ordering = ('visits_count', 'name',)


admin.site.register(Favorite, FavoriteAdmin)
