#!/usr/bin/env python
"""
Test script to verify .env file loading and email configuration
"""
import os
import sys
import django
from django.conf import settings

# Add the project directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'securefiles.settings')
django.setup()

def test_env_loading():
    """Test that environment variables are loaded correctly"""
    
    print("🔍 Testing Environment Variable Loading")
    print("=" * 50)
    
    # Check if .env file exists
    env_file = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(env_file):
        print(f"✅ .env file found at: {env_file}")
        
        # Read .env file content
        with open(env_file, 'r') as f:
            content = f.read()
            print(f"📄 .env file content:")
            for line in content.strip().split('\n'):
                if '=' in line:
                    key, value = line.split('=', 1)
                    if 'PASSWORD' in key:
                        print(f"   {key}={'*' * len(value)}")
                    else:
                        print(f"   {key}={value}")
    else:
        print(f"❌ .env file not found at: {env_file}")
    
    print(f"\n📧 Django Email Configuration:")
    print(f"   EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
    print(f"   EMAIL_HOST: {settings.EMAIL_HOST}")
    print(f"   EMAIL_PORT: {settings.EMAIL_PORT}")
    print(f"   EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
    print(f"   EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
    print(f"   EMAIL_HOST_PASSWORD: {'*' * len(settings.EMAIL_HOST_PASSWORD) if settings.EMAIL_HOST_PASSWORD else 'None'}")
    print(f"   DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
    
    # Check if we're using console backend or SMTP
    if settings.EMAIL_BACKEND == 'django.core.mail.backends.console.EmailBackend':
        print(f"\n⚠️  WARNING: Using console backend - emails will appear in terminal")
        print(f"   This happens when email credentials are not properly configured")
    else:
        print(f"\n✅ Using SMTP backend - emails will be sent to actual recipients")
    
    # Test environment variable loading
    print(f"\n🔧 Environment Variables:")
    email_host = os.getenv('EMAIL_HOST', 'NOT_SET')
    email_user = os.getenv('EMAIL_HOST_USER', 'NOT_SET')
    email_pass = os.getenv('EMAIL_HOST_PASSWORD', 'NOT_SET')
    
    print(f"   EMAIL_HOST: {email_host}")
    print(f"   EMAIL_HOST_USER: {email_user}")
    print(f"   EMAIL_HOST_PASSWORD: {'*' * len(email_pass) if email_pass != 'NOT_SET' else 'NOT_SET'}")
    
    return settings.EMAIL_BACKEND == 'django.core.mail.backends.smtp.EmailBackend'

if __name__ == '__main__':
    success = test_env_loading()
    
    if success:
        print(f"\n🎉 SUCCESS: Email configuration is correct!")
        print(f"   Magic login emails will be sent to actual email addresses")
    else:
        print(f"\n❌ ISSUE: Email configuration needs fixing")
        print(f"   Magic login emails will appear in terminal instead of being sent")
