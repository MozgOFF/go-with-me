from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import ugettext_lazy as _
from .models import User, OTP, SMSMessage, Friendships


# admin.site.register(User)

class FriendshipsInlineAdmin(admin.TabularInline):
    model = Friendships
    fk_name = 'from_user'


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    """Define admin model for custom User model with no email field."""

    fieldsets = (
        (None, {'fields': ('phone', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'telegram_username')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'password1', 'password2'),
        }),
    )
    list_display = ('phone', 'first_name', 'last_name', 'is_staff', 'telegram_username')
    search_fields = ('phone', 'first_name', 'last_name')
    ordering = ('phone',)
    inlines = [FriendshipsInlineAdmin, ]


admin.site.register(OTP)
admin.site.register(SMSMessage)
admin.site.register(Friendships)
