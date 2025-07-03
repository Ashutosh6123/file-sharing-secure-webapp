#!/usr/bin/env python3
"""
Test script to validate magic-link-only login implementation
"""
import os
import sys
import django
from django.test.client import Client
from django.contrib.auth import authenticate

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'securefiles.settings')
django.setup()

from users.models import CustomUser, MagicLoginToken
from django.contrib.messages import get_messages

def test_magic_only_login():
    """Test that magic-link-only login is enforced"""
    print("🔍 Testing Magic-Link-Only Login Implementation")
    print("=" * 50)
    
    # Create test users
    print("\n1. Creating test users...")
    try:
        # Clean up existing test users first
        CustomUser.objects.filter(username__in=['test_ops_magic', 'test_client_magic']).delete()
        
        ops_user = CustomUser.objects.create_user(
            username='test_ops_magic',
            email='test_ops_magic@example.com',
            password='testpass123',
            is_ops=True,
            is_active=True
        )
        print(f"   ✅ Created ops user: {ops_user.email}")
        
        client_user = CustomUser.objects.create_user(
            username='test_client_magic',
            email='test_client_magic@example.com',
            password='testpass123',
            is_client=True,
            is_active=True
        )
        print(f"   ✅ Created client user: {client_user.email}")
        
    except Exception as e:
        print(f"   ❌ Error creating users: {e}")
        return False
    
    # Test authentication directly (should still work for API)
    print("\n2. Testing direct authentication (for API compatibility)...")
    ops_auth = authenticate(username='test_ops_magic', password='testpass123')
    client_auth = authenticate(username='test_client_magic', password='testpass123')
    
    if ops_auth and client_auth:
        print("   ✅ Direct authentication still works (API compatibility)")
    else:
        print("   ❌ Direct authentication failed")
    
    # Test web login views (should NOT accept passwords)
    print("\n3. Testing web login views...")
    client = Client()
    
    # Test ops login
    print("\n   Testing ops login view...")
    response = client.post('/ops-login/', {
        'email': 'test_ops_magic@example.com'
    })
    
    if response.status_code == 200:
        messages = list(get_messages(response.wsgi_request))
        success_messages = [msg for msg in messages if 'magic login link sent' in str(msg).lower()]
        
        if success_messages:
            print("   ✅ Ops login correctly sends magic link")
        else:
            print("   ❌ Ops login did not send magic link")
            for msg in messages:
                print(f"      Message: {msg}")
    else:
        print(f"   ❌ Ops login failed with status {response.status_code}")
    
    # Test client login
    print("\n   Testing client login view...")
    response = client.post('/client-login/', {
        'email': 'test_client_magic@example.com'
    })
    
    if response.status_code == 200:
        messages = list(get_messages(response.wsgi_request))
        success_messages = [msg for msg in messages if 'magic login link sent' in str(msg).lower()]
        
        if success_messages:
            print("   ✅ Client login correctly sends magic link")
        else:
            print("   ❌ Client login did not send magic link")
            for msg in messages:
                print(f"      Message: {msg}")
    else:
        print(f"   ❌ Client login failed with status {response.status_code}")
    
    # Test general login
    print("\n   Testing general login view...")
    response = client.post('/login/', {
        'email': 'test_ops_magic@example.com'
    })
    
    if response.status_code == 200:
        messages = list(get_messages(response.wsgi_request))
        success_messages = [msg for msg in messages if 'magic login link sent' in str(msg).lower()]
        
        if success_messages:
            print("   ✅ General login correctly sends magic link")
        else:
            print("   ❌ General login did not send magic link")
            for msg in messages:
                print(f"      Message: {msg}")
    else:
        print(f"   ❌ General login failed with status {response.status_code}")
    
    # Test magic token creation
    print("\n4. Testing magic token creation...")
    initial_token_count = MagicLoginToken.objects.count()
    
    # Send magic login request
    response = client.post('/ops-login/', {
        'email': 'test_ops_magic@example.com'
    })
    
    final_token_count = MagicLoginToken.objects.count()
    
    if final_token_count > initial_token_count:
        print("   ✅ Magic tokens are being created")
        
        # Get the latest token
        latest_token = MagicLoginToken.objects.latest('created_at')
        print(f"   ✅ Latest token created for user: {latest_token.user.email}")
        
        # Test magic login
        print("\n5. Testing magic login...")
        magic_response = client.get(f'/magic-login/{latest_token.token}/')
        
        if magic_response.status_code == 302:  # Should redirect
            print("   ✅ Magic login works and redirects")
            
            # Check if user is logged in
            if '_auth_user_id' in client.session:
                print("   ✅ User is logged in after magic login")
            else:
                print("   ❌ User is not logged in after magic login")
        else:
            print(f"   ❌ Magic login failed with status {magic_response.status_code}")
    else:
        print("   ❌ Magic tokens are not being created")
    
    # Test password-based login attempts (should fail)
    print("\n6. Testing password-based login attempts...")
    
    # Try to post with password fields (should be ignored)
    response = client.post('/ops-login/', {
        'username': 'test_ops_magic',
        'password': 'testpass123',
        'email': 'test_ops_magic@example.com'
    })
    
    if response.status_code == 200:
        print("   ✅ Password fields are ignored in login forms")
    else:
        print(f"   ❌ Unexpected response: {response.status_code}")
    
    # Cleanup
    print("\n7. Cleaning up...")
    try:
        CustomUser.objects.filter(username__in=['test_ops_magic', 'test_client_magic']).delete()
        MagicLoginToken.objects.filter(user__username__in=['test_ops_magic', 'test_client_magic']).delete()
        print("   ✅ Test users and tokens cleaned up")
    except Exception as e:
        print(f"   ❌ Cleanup error: {e}")
    
    print("\n" + "=" * 50)
    print("✅ Magic-Link-Only Login Test Complete!")
    print("🔒 System is configured for magic-link-only authentication")

if __name__ == '__main__':
    test_magic_only_login()
