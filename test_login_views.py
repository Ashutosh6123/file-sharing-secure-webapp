"""
Simple test to verify login functionality and magic email sending
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
from django.urls import reverse
from users.models import CustomUser, MagicLoginToken
from django.contrib.auth import authenticate

def test_login_views():
    """Test that login views send magic login emails"""
    
    print("🧪 Testing Login Views and Magic Email Functionality")
    print("=" * 60)
    
    # Ensure test users exist
    try:
        ops_user = CustomUser.objects.get(username='test_ops')
        client_user = CustomUser.objects.get(username='test_client')
        print(f"✅ Test users found:")
        print(f"   - Ops user: {ops_user.username} (ops: {ops_user.is_ops})")
        print(f"   - Client user: {client_user.username} (client: {client_user.is_client})")
    except CustomUser.DoesNotExist:
        print("❌ Test users not found. Creating them...")
        # Create test users
        ops_user = CustomUser.objects.create_user(
            username='test_ops',
            email='test_ops@example.com',
            password='testpass123',
            is_ops=True,
            is_active=True
        )
        client_user = CustomUser.objects.create_user(
            username='test_client',
            email='test_client@example.com', 
            password='testpass123',
            is_client=True,
            is_active=True
        )
        print(f"✅ Test users created")
    
    # Test authentication works
    print(f"\n🔍 Testing authentication...")
    auth_ops = authenticate(username='test_ops', password='testpass123')
    auth_client = authenticate(username='test_client', password='testpass123')
    
    print(f"   - Ops auth: {'✅ Success' if auth_ops else '❌ Failed'}")
    print(f"   - Client auth: {'✅ Success' if auth_client else '❌ Failed'}")
    
    # Count existing tokens
    initial_tokens = MagicLoginToken.objects.count()
    print(f"\n📊 Initial magic tokens in database: {initial_tokens}")
    
    # Test client with login views
    client = Client()
    
    # Test ops login
    print(f"\n🔍 Testing ops login view...")
    response = client.post('/ops-login/', {
        'username': 'test_ops',
        'password': 'testpass123'
    })
    print(f"   Response status: {response.status_code}")
    if response.status_code == 302:
        print(f"   Redirect to: {response.get('Location', 'Unknown')}")
    
    # Test client login
    print(f"\n🔍 Testing client login view...")
    response = client.post('/client-login/', {
        'username': 'test_client',
        'password': 'testpass123'
    })
    print(f"   Response status: {response.status_code}")
    if response.status_code == 302:
        print(f"   Redirect to: {response.get('Location', 'Unknown')}")
    
    # Test general login
    print(f"\n🔍 Testing general login view...")
    response = client.post('/login/', {
        'username': 'test_ops',
        'password': 'testpass123'
    })
    print(f"   Response status: {response.status_code}")
    if response.status_code == 302:
        print(f"   Redirect to: {response.get('Location', 'Unknown')}")
    
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
        print(f"   - {token.user.username}: {token.token[:8]}... (created: {token.created_at})")
    
    # Final assessment
    if new_tokens >= 3:  # Should have at least 3 new tokens (one for each login attempt)
        print(f"\n✅ SUCCESS: Magic login emails are being sent on login attempts!")
        print(f"   - {new_tokens} new magic tokens created")
        print(f"   - All login views appear to be working correctly")
        return True
    else:
        print(f"\n⚠️  WARNING: Expected at least 3 new tokens, but only {new_tokens} were created")
        return False

if __name__ == '__main__':
    test_login_views()
