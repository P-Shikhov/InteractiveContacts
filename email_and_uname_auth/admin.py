from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active',)
    list_filter = ('username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('username', 'first_name', 'last_name', 'email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('username', 'first_name', 'last_name', 'email',)
    ordering = ('username',)

admin.site.register(CustomUser, CustomUserAdmin)