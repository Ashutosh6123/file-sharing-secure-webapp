from django.core.management.base import BaseCommand
from django.contrib.auth import authenticate
from users.models import CustomUser
from users.utils import send_magic_login_email
from django.test import RequestFactory

class Command(BaseCommand):
    help = 'Test magic login email functionality for both user types'

    def handle(self, *args, **options):
        self.stdout.write('🧪 Testing Magic Login Email System...\n')
        
        # Create a mock request
        factory = RequestFactory()
        request = factory.get('/')
        request.META['HTTP_X_FORWARDED_FOR'] = '127.0.0.1'
        request.META['HTTP_USER_AGENT'] = 'Test Browser'
        
        # Test for existing users
        ops_users = CustomUser.objects.filter(is_ops=True, is_active=True)[:1]
        client_users = CustomUser.objects.filter(is_client=True, is_active=True)[:1]
        
        if ops_users:
            ops_user = ops_users[0]
            self.stdout.write(f'📧 Testing Operations User: {ops_user.username} ({ops_user.email})')
            success, message = send_magic_login_email(ops_user, request)
            if success:
                self.stdout.write(self.style.SUCCESS(f'  ✅ {message}'))
            else:
                self.stdout.write(self.style.ERROR(f'  ❌ {message}'))
        else:
            self.stdout.write(self.style.WARNING('  ⚠️ No Operations users found'))
        
        if client_users:
            client_user = client_users[0]
            self.stdout.write(f'📧 Testing Client User: {client_user.username} ({client_user.email})')
            success, message = send_magic_login_email(client_user, request)
            if success:
                self.stdout.write(self.style.SUCCESS(f'  ✅ {message}'))
            else:
                self.stdout.write(self.style.ERROR(f'  ❌ {message}'))
        else:
            self.stdout.write(self.style.WARNING('  ⚠️ No Client users found'))
        
        self.stdout.write('\n📝 Summary:')
        self.stdout.write('- Magic login emails are now sent to BOTH Operations and Client users')
        self.stdout.write('- Emails are sent on ALL login attempts (ops_login, client_login, user_login)')
        self.stdout.write('- Magic links redirect to appropriate dashboards based on user type')
        self.stdout.write('- Request magic login page supports both user types')
        
        self.stdout.write(f'\n🔧 Current Email Configuration:')
        from django.conf import settings
        self.stdout.write(f'  Backend: {settings.EMAIL_BACKEND}')
        if hasattr(settings, 'EMAIL_HOST_USER'):
            self.stdout.write(f'  Host User: {settings.EMAIL_HOST_USER}')
            self.stdout.write(f'  Host: {settings.EMAIL_HOST}')
            self.stdout.write(f'  Port: {settings.EMAIL_PORT}')
            self.stdout.write(f'  TLS: {settings.EMAIL_USE_TLS}')
