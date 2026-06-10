import requests
import json

url = "http://127.0.0.1:8000/api/v1/auth/login"

# Test with username
data = {"username": "admin", "password": "admin123"}
print("Testing login...")
response = requests.post(url, json=data)

print(f"Status: {response.status_code}")
if response.status_code == 200:
    result = response.json()
    print(f"✅ Login successful!")
    print(f"   Username: {result['username']}")
    print(f"   Role: {result['role']}")
    print(f"   Token: {result['access_token'][:50]}...")
else:
    print(f"❌ Failed: {response.text}")
