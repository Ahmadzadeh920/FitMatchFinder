from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin



class CustomUserAdmin(BaseUserAdmin):
    # Define the fields to be used in displaying the CustomUser model.
    list_display = ('email', 'is_staff', 'is_active', 'is_verified', 'created_at', 'updated_at')
    list_filter = ('is_staff', 'is_active', 'is_verified')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_verified', 'is_superuser')}),
        ('Important dates', {'fields': ('created_at', 'updated_at')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active', 'is_verified')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

# Register the custom user model with the admin site
admin.site.register(CustomUser, CustomUserAdmin)