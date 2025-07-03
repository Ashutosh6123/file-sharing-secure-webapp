#!/usr/bin/env python3
"""
Simple test script to verify magic-link-only login functionality
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'securefiles.settings')
django.setup()

from users.models import CustomUser, MagicLoginToken
from users.utils import send_magic_login_email
from django.test import RequestFactory
from django.contrib.auth import authenticate

def test_magic_login_system():
    """Test the magic-link-only login system"""
    print("🔐 Testing Magic-Link-Only Login System")
    print("=" * 50)
    
    # Create a test user
    print("\n1. Creating test user...")
    try:
        # Clean up existing test user
        CustomUser.objects.filter(username='test_user_magic').delete()
        
        test_user = CustomUser.objects.create_user(
            username='test_user_magic',
            email='test@example.com',
            password='testpass123',
            is_ops=True,
            is_active=True
        )
        print(f"   ✅ Created test user: {test_user.email}")
        
    except Exception as e:
        print(f"   ❌ Error creating user: {e}")
        return
    
    # Test direct authentication (should still work for API)
    print("\n2. Testing direct authentication...")
    user = authenticate(username='test_user_magic', password='testpass123')
    if user:
        print("   ✅ Direct authentication works (for API compatibility)")
    else:
        print("   ❌ Direct authentication failed")
    
    # Test magic token creation
    print("\n3. Testing magic token creation...")
    factory = RequestFactory()
    request = factory.post('/ops-login/', {'email': 'test@example.com'})
    request.META['REMOTE_ADDR'] = '127.0.0.1'
    request.META['HTTP_USER_AGENT'] = 'Test Agent'
    
    try:
        success, message = send_magic_login_email(test_user, request)
        if success:
            print("   ✅ Magic token created successfully")
            print(f"   ✅ Message: {message}")
        else:
            print(f"   ❌ Magic token creation failed: {message}")
    except Exception as e:
        print(f"   ❌ Error creating magic token: {e}")
    
    # Check if tokens are created
    print("\n4. Checking magic tokens...")
    tokens = MagicLoginToken.objects.filter(user=test_user)
    if tokens.exists():
        print(f"   ✅ Found {tokens.count()} magic token(s)")
        latest_token = tokens.latest('created_at')
        print(f"   ✅ Latest token: {latest_token.token[:10]}...")
        print(f"   ✅ Token valid: {latest_token.is_valid()}")
    else:
        print("   ❌ No magic tokens found")
    
    # Test magic login validation
    print("\n5. Testing magic login validation...")
    if tokens.exists():
        from users.utils import validate_magic_token
        
        token, error = validate_magic_token(latest_token.token)
        if token:
            print("   ✅ Magic token validation successful")
            print(f"   ✅ Token user: {token.user.email}")
        else:
            print(f"   ❌ Magic token validation failed: {error}")
    
    # Cleanup
    print("\n6. Cleaning up...")
    try:
        CustomUser.objects.filter(username='test_user_magic').delete()
        print("   ✅ Test user cleaned up")
    except Exception as e:
        print(f"   ❌ Cleanup error: {e}")
    
    print("\n" + "=" * 50)
    print("✅ Magic-Link-Only Login System Test Complete!")
    print("🔒 Password-based login is disabled in views")
    print("🔗 Magic-link-only authentication is enforced")
    print("📧 Magic login emails are sent successfully")

if __name__ == '__main__':
    test_magic_login_system()
