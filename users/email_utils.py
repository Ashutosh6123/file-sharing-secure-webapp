from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
import traceback

def test_email_configuration():
    """Test if email configuration is working properly"""
    try:
        # Simple test email
        subject = '🧪 Email Configuration Test - Secure File Share'
        message = '''
This is a test email to verify that your SMTP configuration is working correctly.

Email Settings:
- Backend: {backend}
- Host: {host}
- Port: {port}
- TLS: {tls}
- From: {from_email}

If you received this email, your configuration is working properly!

Best regards,
Secure File Share System
        '''.format(
            backend=settings.EMAIL_BACKEND,
            host=getattr(settings, 'EMAIL_HOST', 'Not configured'),
            port=getattr(settings, 'EMAIL_PORT', 'Not configured'),
            tls=getattr(settings, 'EMAIL_USE_TLS', 'Not configured'),
            from_email=settings.DEFAULT_FROM_EMAIL
        )
        
        # Send test email
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.EMAIL_HOST_USER],  # Send to configured email
            fail_silently=False,
        )
        
        return True, "Test email sent successfully!"
        
    except Exception as e:
        error_msg = f"Email configuration test failed: {str(e)}"
        print(f"Full error traceback:\n{traceback.format_exc()}")
        return False, error_msg

def send_email_with_retry(subject, message, recipient_list, html_message=None, max_retries=3):
    """Send email with retry mechanism"""
    for attempt in range(max_retries):
        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=recipient_list,
                html_message=html_message,
                fail_silently=False,
            )
            return True, "Email sent successfully"
            
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"Email attempt {attempt + 1} failed: {str(e)}. Retrying...")
                continue
            else:
                error_msg = f"Failed to send email after {max_retries} attempts: {str(e)}"
                print(f"Full error traceback:\n{traceback.format_exc()}")
                return False, error_msg
    
    return False, "Unknown error occurred"

def get_email_provider_settings(provider):
    """Get SMTP settings for common email providers"""
    providers = {
        'gmail': {
            'EMAIL_HOST': 'smtp.gmail.com',
            'EMAIL_PORT': 587,
            'EMAIL_USE_TLS': True,
            'instructions': '''
For Gmail:
1. Enable 2-Factor Authentication
2. Generate an App Password:
   - Go to Google Account settings
   - Security → 2-Step Verification → App passwords
   - Generate password for "Mail"
3. Use the app password in EMAIL_HOST_PASSWORD
            '''
        },
        'outlook': {
            'EMAIL_HOST': 'smtp-mail.outlook.com',
            'EMAIL_PORT': 587,
            'EMAIL_USE_TLS': True,
            'instructions': '''
For Outlook/Hotmail:
1. Use your regular email and password
2. May need to enable "Less secure app access"
            '''
        },
        'yahoo': {
            'EMAIL_HOST': 'smtp.mail.yahoo.com',
            'EMAIL_PORT': 587,
            'EMAIL_USE_TLS': True,
            'instructions': '''
For Yahoo:
1. Enable 2-Factor Authentication
2. Generate an App Password:
   - Go to Account Security
   - Generate and manage app passwords
   - Create password for "Mail"
            '''
        }
    }
    
    return providers.get(provider.lower(), {})
