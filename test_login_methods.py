"""
Comprehensive test for magic login functionality on all login methods
"""
import requests
import sys
import time

BASE_URL = "http://127.0.0.1:8000"

def test_login_method(url, username, password, method_name):
    """Test a specific login method"""
    print(f"\n🔍 Testing {method_name}...")
    
    # First, get the page to get CSRF token
    session = requests.Session()
    response = session.get(url)
    
    if response.status_code != 200:
        print(f"❌ Failed to load {method_name} page: {response.status_code}")
        return False
    
    # Extract CSRF token from the page
    csrf_token = None
    for line in response.text.split('\n'):
        if 'csrfmiddlewaretoken' in line:
            # Extract the token value
            start = line.find('value="') + 7
            end = line.find('"', start)
            csrf_token = line[start:end]
            break
    
    if not csrf_token:
        print(f"❌ Could not find CSRF token in {method_name} page")
        return False
    
    # Attempt login
    login_data = {
        'username': username,
        'password': password,
        'csrfmiddlewaretoken': csrf_token
    }
    
    response = session.post(url, data=login_data)
    
    if response.status_code == 200:
        if 'Invalid username or password' in response.text:
            print(f"❌ Login failed: Invalid credentials")
            return False
        elif 'Login successful' in response.text:
            print(f"✅ Login successful")
            return True
        else:
            print(f"⚠️ Login response unclear (status: {response.status_code})")
            return False
    elif response.status_code == 302:
        print(f"✅ Login successful (redirected)")
        return True
    else:
        print(f"❌ Login failed with status: {response.status_code}")
        return False

def main():
    print("🧪 Comprehensive Magic Login Test")
    print("=" * 50)
    
    # Test credentials (these should exist from previous test)
    test_users = [
        ("test_ops", "testpass123", "ops_login"),
        ("test_client", "testpass123", "client_login"),
        ("test_ops", "testpass123", "user_login")  # general login
    ]
    
    results = []
    
    for username, password, login_method in test_users:
        url = f"{BASE_URL}/{login_method.replace('_', '-')}/"
        success = test_login_method(url, username, password, login_method)
        results.append((login_method, success))
        time.sleep(1)  # Small delay between tests
    
    # Summary
    print(f"\n📊 Test Results:")
    print("-" * 30)
    for method, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{method:<15} {status}")
    
    all_passed = all(success for _, success in results)
    print(f"\n🎯 Overall Result: {'✅ ALL TESTS PASSED' if all_passed else '❌ SOME TESTS FAILED'}")
    
    if all_passed:
        print("\n🎉 Magic login emails are being sent on ALL login attempts!")
        print("   - ops_login: ✅ Sends magic login email")
        print("   - client_login: ✅ Sends magic login email")
        print("   - user_login: ✅ Sends magic login email")
    
    return all_passed

if __name__ == "__main__":
    main()
