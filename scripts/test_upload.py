import requests
import json

# First, login to get token
login_data = {
    "username": "ayush123",
    "password": "test123"  # Try common passwords
}

print("🔐 Logging in...")
response = requests.post('http://localhost:5000/auth/login', json=login_data)
print(f"Login status: {response.status_code}")

if response.status_code != 200:
    # Try another password
    login_data["password"] = "password"
    response = requests.post('http://localhost:5000/auth/login', json=login_data)
    print(f"Login status (attempt 2): {response.status_code}")

if response.status_code != 200:
    print("❌ Login failed! Please run this script manually with your password")
    print("Edit test_upload.py and set the correct password")
    exit(1)

print(f"Response: {response.json()}")

if response.status_code == 200:
    token = response.json()['access_token']
    print(f"\n✅ Token received: {token[:20]}...")
    
    # Test upload endpoint
    print("\n📤 Testing upload endpoint...")
    headers = {
        'Authorization': f'Bearer {token}'
    }
    
    # Create a test file
    files = {
        'file': ('test.jpg', b'fake image data', 'image/jpeg')
    }
    
    response = requests.post(
        'http://localhost:5000/photos/upload',
        headers=headers,
        files=files
    )
    
    print(f"Upload status: {response.status_code}")
    print(f"Response: {response.text}")
else:
    print("❌ Login failed!")
