#!/usr/bin/env python
"""
Test script to verify magic login email functionality for all login methods
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

from django.test import RequestFactory, Client
from django.contrib.auth import authenticate
from users.models import CustomUser, MagicLoginToken
from users.utils import send_magic_login_email
from unittest.mock import patch
import io
import sys

def test_magic_login_functionality():
    """Test that magic login emails are sent for all login methods"""
    
    print("🔍 Testing Magic Login Email Functionality")
    print("=" * 50)
    
    # Setup test users
    try:
        # Create test users if they don't exist
        ops_user, created = CustomUser.objects.get_or_create(
            username='test_ops',
            defaults={
                'email': 'test_ops@example.com',
                'is_ops': True,
                'is_active': True
            }
        )
        if created:
            ops_user.set_password('testpass123')
            ops_user.save()
        
        client_user, created = CustomUser.objects.get_or_create(
            username='test_client', 
            defaults={
                'email': 'test_client@example.com',
                'is_client': True,
                'is_active': True
            }
        )
        if created:
            client_user.set_password('testpass123')
            client_user.save()
            
        print(f"✅ Test users created/verified:")
        print(f"   - Ops user: {ops_user.username} ({ops_user.email})")
        print(f"   - Client user: {client_user.username} ({client_user.email})")
        
    except Exception as e:
        print(f"❌ Error creating test users: {e}")
        return False
    
    # Test magic login email utility function
    factory = RequestFactory()
    request = factory.get('/')
    request.META['REMOTE_ADDR'] = '127.0.0.1'
    request.META['HTTP_USER_AGENT'] = 'Test Browser'
    
    # Test ops user
    print(f"\n🔍 Testing magic login for ops user...")
    success, message = send_magic_login_email(ops_user, request)
    print(f"   Result: {'✅ Success' if success else '❌ Failed'}")
    print(f"   Message: {message}")
    
    # Test client user 
    print(f"\n🔍 Testing magic login for client user...")
    success, message = send_magic_login_email(client_user, request)
    print(f"   Result: {'✅ Success' if success else '❌ Failed'}")
    print(f"   Message: {message}")
    
    # Check if tokens were created
    ops_tokens = MagicLoginToken.objects.filter(user=ops_user, is_used=False)
    client_tokens = MagicLoginToken.objects.filter(user=client_user, is_used=False)
    
    print(f"\n📝 Magic tokens created:")
    print(f"   - Ops user tokens: {ops_tokens.count()}")
    print(f"   - Client user tokens: {client_tokens.count()}")
    
    # Test Django Client for login views
    client = Client()
    
    print(f"\n🔍 Testing login views...")
    
    # Test ops login view
    print(f"   Testing ops login view...")
    response = client.post('/ops-login/', {
        'username': 'test_ops',
        'password': 'testpass123'
    })
    print(f"   Ops login response: {response.status_code}")
    
    # Test client login view  
    print(f"   Testing client login view...")
    response = client.post('/client-login/', {
        'username': 'test_client', 
        'password': 'testpass123'
    })
    print(f"   Client login response: {response.status_code}")
    
    # Test general login view
    print(f"   Testing general login view...")
    response = client.post('/login/', {
        'username': 'test_ops',
        'password': 'testpass123'
    })
    print(f"   General login response: {response.status_code}")
    
    # Check final token count
    total_tokens = MagicLoginToken.objects.filter(is_used=False).count()
    print(f"\n📊 Total unused magic tokens: {total_tokens}")
    
    return True

if __name__ == '__main__':
    test_magic_login_functionality()
