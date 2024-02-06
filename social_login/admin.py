from django.contrib import admin
from .models import User


class SocialLoginAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ('email', 'nickname', 'profile')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Game Data', {'fields': ('win', 'lose', 'rank')}),
    ]
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'nickname'),
        }),
    )
    list_display = ('email', 'nickname', 'profile')
    search_fields = ('email', 'nickname')
    ordering = ('created_at',)


admin.site.register(User, SocialLoginAdmin)
