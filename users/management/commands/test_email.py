from django.core.management.base import BaseCommand
from django.conf import settings
from users.email_utils import test_email_configuration, get_email_provider_settings

class Command(BaseCommand):
    help = 'Test email configuration and send a test email'

    def add_arguments(self, parser):
        parser.add_argument(
            '--provider',
            type=str,
            choices=['gmail', 'outlook', 'yahoo'],
            help='Show configuration instructions for specific email provider',
        )
        parser.add_argument(
            '--test',
            action='store_true',
            help='Send a test email to verify configuration',
        )

    def handle(self, *args, **options):
        if options['provider']:
            provider = options['provider']
            settings_info = get_email_provider_settings(provider)
            
            if settings_info:
                self.stdout.write(
                    self.style.SUCCESS(f'\n📧 Email Configuration for {provider.title()}:')
                )
                self.stdout.write(f"EMAIL_HOST = '{settings_info['EMAIL_HOST']}'")
                self.stdout.write(f"EMAIL_PORT = {settings_info['EMAIL_PORT']}")
                self.stdout.write(f"EMAIL_USE_TLS = {settings_info['EMAIL_USE_TLS']}")
                self.stdout.write(settings_info['instructions'])
            else:
                self.stdout.write(
                    self.style.ERROR(f'No configuration found for provider: {provider}')
                )
            return

        # Show current configuration
        self.stdout.write(self.style.SUCCESS('\n📧 Current Email Configuration:'))
        self.stdout.write(f"Backend: {settings.EMAIL_BACKEND}")
        
        if hasattr(settings, 'EMAIL_HOST'):
            self.stdout.write(f"Host: {settings.EMAIL_HOST}")
            self.stdout.write(f"Port: {settings.EMAIL_PORT}")
            self.stdout.write(f"TLS: {settings.EMAIL_USE_TLS}")
            self.stdout.write(f"User: {settings.EMAIL_HOST_USER}")
            self.stdout.write(f"From: {settings.DEFAULT_FROM_EMAIL}")
        
        # Test email if requested
        if options['test']:
            self.stdout.write('\n🧪 Testing email configuration...')
            
            if settings.EMAIL_BACKEND == 'django.core.mail.backends.console.EmailBackend':
                self.stdout.write(
                    self.style.WARNING(
                        'Currently using console backend. Emails will appear in terminal, not sent via SMTP.'
                    )
                )
            else:
                success, message = test_email_configuration()
                
                if success:
                    self.stdout.write(self.style.SUCCESS(f'✅ {message}'))
                else:
                    self.stdout.write(self.style.ERROR(f'❌ {message}'))
                    
                    # Provide troubleshooting tips
                    self.stdout.write('\n🔧 Troubleshooting Tips:')
                    self.stdout.write('1. Check EMAIL_HOST_USER and EMAIL_HOST_PASSWORD')
                    self.stdout.write('2. For Gmail: Use App Password, not regular password')
                    self.stdout.write('3. Ensure EMAIL_USE_TLS is set correctly')
                    self.stdout.write('4. Check firewall and network connectivity')
                    self.stdout.write('5. Verify email provider SMTP settings')
        else:
            self.stdout.write('\nUse --test flag to send a test email')
            self.stdout.write('Use --provider gmail/outlook/yahoo for setup instructions')
