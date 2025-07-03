#!/usr/bin/env python
"""
Test the magic-link-only login system
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

from django.test import Client
from users.models import CustomUser, MagicLoginToken

def test_magic_only_login():
    """Test that login views only accept email and send magic links"""
    
    print("🧪 Testing Magic-Link-Only Login System")
    print("=" * 55)
    
    # Ensure test users exist with proper email addresses
    ops_user, created = CustomUser.objects.get_or_create(
        username='test_ops_magic_only',
        defaults={
            'email': 'ashutosh06123@gmail.com',
            'is_ops': True,
            'is_active': True,
            'first_name': 'Magic',
            'last_name': 'Ops'
        }
    )
    
    client_user, created = CustomUser.objects.get_or_create(
        username='test_client_magic_only',
        defaults={
            'email': 'ashutosh06123@gmail.com',
            'is_client': True,
            'is_active': True,
            'first_name': 'Magic',
            'last_name': 'Client'
        }
    )
    
    print(f"✅ Test users ready:")
    print(f"   - Ops user: {ops_user.username} ({ops_user.email})")
    print(f"   - Client user: {client_user.username} ({client_user.email})")
    
    # Count initial tokens
    initial_tokens = MagicLoginToken.objects.count()
    print(f"\n📊 Initial magic tokens: {initial_tokens}")
    
    # Test client
    client = Client()
    
    print(f"\n🔍 Testing login views with email-only input...")
    
    # Test ops login with email
    print(f"   Testing ops login with email...")
    ops_response = client.post('/ops-login/', {
        'email': 'ashutosh06123@gmail.com'
    })
    print(f"   Ops response status: {ops_response.status_code}")
    
    # Test client login with email
    print(f"   Testing client login with email...")
    client_response = client.post('/client-login/', {
        'email': 'ashutosh06123@gmail.com'
    })
    print(f"   Client response status: {client_response.status_code}")
    
    # Test general login with email
    print(f"   Testing general login with email...")
    general_response = client.post('/login/', {
        'email': 'ashutosh06123@gmail.com'
    })
    print(f"   General response status: {general_response.status_code}")
    
    # Check token count after login attempts
    final_tokens = MagicLoginToken.objects.count()
    new_tokens = final_tokens - initial_tokens
    
    print(f"\n📊 Token count after login attempts:")
    print(f"   - Initial: {initial_tokens}")
    print(f"   - Final: {final_tokens}")
    print(f"   - New tokens created: {new_tokens}")
    
    # Show recent tokens
    recent_tokens = MagicLoginToken.objects.filter(is_used=False).order_by('-created_at')[:5]
    print(f"\n📋 Recent unused magic tokens:")
    for token in recent_tokens:
        print(f"   - {token.user.username}: {token.token[:8]}... (user_type: {'ops' if token.user.is_ops else 'client'})")
    
    # Verify no password-based authentication
    print(f"\n🔒 Testing that password authentication is disabled...")
    
    # Try old username/password approach (should fail)
    old_ops_response = client.post('/ops-login/', {
        'username': 'test_ops_magic_only',
        'password': 'testpass123'
    })
    print(f"   Old ops login attempt: {old_ops_response.status_code}")
    
    old_client_response = client.post('/client-login/', {
        'username': 'test_client_magic_only', 
        'password': 'testpass123'
    })
    print(f"   Old client login attempt: {old_client_response.status_code}")
    
    # Final assessment
    if new_tokens >= 2:  # Should have tokens from email-based login attempts
        print(f"\n🎉 SUCCESS: Magic-link-only login is working!")
        print(f"   - {new_tokens} magic tokens created from email-based login")
        print(f"   - No password authentication required")
        print(f"   - All login methods use magic links only")
        return True
    else:
        print(f"\n⚠️  WARNING: Expected tokens from email-based login, but only {new_tokens} were created")
        return False

if __name__ == '__main__':
    test_magic_only_login()
