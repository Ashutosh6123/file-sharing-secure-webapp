#!/usr/bin/env python
"""
Test magic login redirection for both ops and client users
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
from users.utils import send_magic_login_email
from django.test import RequestFactory

def test_magic_login_redirection():
    """Test that magic login redirects to correct dashboards"""
    
    print("🧪 Testing Magic Login Redirection")
    print("=" * 50)
    
    # Setup test data
    factory = RequestFactory()
    request = factory.get('/')
    request.META['REMOTE_ADDR'] = '127.0.0.1'
    request.META['HTTP_USER_AGENT'] = 'Test Browser'
    
    # Ensure test users exist with proper email addresses
    ops_user, created = CustomUser.objects.get_or_create(
        username='test_ops_redirect',
        defaults={
            'email': 'ashutosh06123@gmail.com',
            'is_ops': True,
            'is_active': True,
            'first_name': 'Test',
            'last_name': 'Ops'
        }
    )
    
    client_user, created = CustomUser.objects.get_or_create(
        username='test_client_redirect',
        defaults={
            'email': 'ashutosh06123@gmail.com',
            'is_client': True,
            'is_active': True,
            'first_name': 'Test',
            'last_name': 'Client'
        }
    )
    
    print(f"✅ Test users ready:")
    print(f"   - Ops user: {ops_user.username} (is_ops: {ops_user.is_ops})")
    print(f"   - Client user: {client_user.username} (is_client: {client_user.is_client})")
    
    # Generate magic tokens
    print(f"\n🔗 Generating magic login tokens...")
    
    ops_success, ops_message = send_magic_login_email(ops_user, request)
    client_success, client_message = send_magic_login_email(client_user, request)
    
    print(f"   - Ops token: {'✅ Created' if ops_success else '❌ Failed'}")
    print(f"   - Client token: {'✅ Created' if client_success else '❌ Failed'}")
    
    # Get the generated tokens
    ops_token = MagicLoginToken.objects.filter(user=ops_user, is_used=False).last()
    client_token = MagicLoginToken.objects.filter(user=client_user, is_used=False).last()
    
    if not ops_token or not client_token:
        print("❌ Failed to generate magic tokens")
        return False
    
    print(f"\n📋 Generated tokens:")
    print(f"   - Ops token: {ops_token.token[:8]}...")
    print(f"   - Client token: {client_token.token[:8]}...")
    
    # Test magic login redirection using Django test client
    client = Client()
    
    print(f"\n🧪 Testing magic login redirection...")
    
    # Test ops user magic login
    print(f"   Testing ops user magic login...")
    ops_response = client.get(f'/magic-login/{ops_token.token}/')
    print(f"   Ops response status: {ops_response.status_code}")
    if ops_response.status_code == 302:
        redirect_url = ops_response.get('Location', '')
        print(f"   Ops redirect URL: {redirect_url}")
        if 'dashboard-ops' in redirect_url:
            print(f"   ✅ Ops user redirected to operations dashboard")
        else:
            print(f"   ❌ Ops user redirected to wrong location: {redirect_url}")
    
    # Test client user magic login
    print(f"   Testing client user magic login...")
    client_response = client.get(f'/magic-login/{client_token.token}/')
    print(f"   Client response status: {client_response.status_code}")
    if client_response.status_code == 302:
        redirect_url = client_response.get('Location', '')
        print(f"   Client redirect URL: {redirect_url}")
        if 'dashboard-client' in redirect_url:
            print(f"   ✅ Client user redirected to client dashboard")
        else:
            print(f"   ❌ Client user redirected to wrong location: {redirect_url}")
    
    # Check if tokens are marked as used
    ops_token.refresh_from_db()
    client_token.refresh_from_db()
    
    print(f"\n📊 Token usage status:")
    print(f"   - Ops token used: {'✅ Yes' if ops_token.is_used else '❌ No'}")
    print(f"   - Client token used: {'✅ Yes' if client_token.is_used else '❌ No'}")
    
    # Final assessment
    ops_correct = ops_response.status_code == 302 and 'dashboard-ops' in ops_response.get('Location', '')
    client_correct = client_response.status_code == 302 and 'dashboard-client' in client_response.get('Location', '')
    
    if ops_correct and client_correct:
        print(f"\n🎉 SUCCESS: Magic login redirection working correctly!")
        print(f"   - Ops users → Operations dashboard ✅")
        print(f"   - Client users → Client dashboard ✅")
        return True
    else:
        print(f"\n❌ ISSUES FOUND:")
        if not ops_correct:
            print(f"   - Ops user redirection issue")
        if not client_correct:
            print(f"   - Client user redirection issue")
        return False

if __name__ == '__main__':
    test_magic_login_redirection()
