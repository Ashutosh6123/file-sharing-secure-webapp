from django.contrib import admin
from .models import CustomUser, MagicLoginToken

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_ops', 'is_client', 'is_active', 'date_joined']
    list_filter = ['is_ops', 'is_client', 'is_active', 'email_verified', 'date_joined']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    readonly_fields = ['date_joined', 'last_login']
    
    fieldsets = (
        ('User Information', {
            'fields': ('username', 'email', 'first_name', 'last_name')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'is_ops', 'is_client', 'email_verified')
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
    )

@admin.register(MagicLoginToken)
class MagicLoginTokenAdmin(admin.ModelAdmin):
    list_display = ['user', 'token_preview', 'created_at', 'expires_at', 'is_used', 'is_valid_status', 'login_ip']
    list_filter = ['is_used', 'created_at', 'expires_at']
    search_fields = ['user__username', 'user__email', 'token', 'login_ip']
    readonly_fields = ['token', 'created_at', 'expires_at', 'is_valid_status']
    ordering = ['-created_at']
    
    def token_preview(self, obj):
        return f"{obj.token[:8]}...{obj.token[-8:]}"
    token_preview.short_description = 'Token Preview'
    
    def is_valid_status(self, obj):
        return "✅ Valid" if obj.is_valid() else "❌ Invalid"
    is_valid_status.short_description = 'Status'
    
    fieldsets = (
        ('Token Information', {
            'fields': ('user', 'token', 'is_valid_status')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'expires_at', 'is_used')
        }),
        ('Login Details', {
            'fields': ('login_ip', 'user_agent')
        }),
    )
