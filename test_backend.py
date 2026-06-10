#!/usr/bin/env python3
"""
Backend Test Script - Run this on your computer to test API endpoints
Usage: python test_backend.py
"""

import requests
import json
from datetime import datetime

# Change this to your server IP
BASE_URL = "http://192.168.8.142:8000"

def test_health():
    print("\n" + "="*50)
    print("1. Testing Health Check")
    print("="*50)
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"✅ Health check: {response.status_code}")
        print(f"   Response: {response.json()}")
        return True
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

def test_login():
    print("\n" + "="*50)
    print("2. Testing Login")
    print("="*50)
    try:
        login_data = {
            "username": "admin@driversafety.com",
            "password": "admin123"  # Change to your password
        }
        response = requests.post(f"{BASE_URL}/api/v1/auth/login", json=login_data)
        print(f"Login response: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Login successful!")
            print(f"   User ID: {data.get('user_id')}")
            print(f"   Is Admin: {data.get('is_admin')}")
            return data.get('access_token'), data.get('user_id')
        else:
            print(f"❌ Login failed: {response.text}")
            return None, None
    except Exception as e:
        print(f"❌ Login error: {e}")
        return None, None

def test_create_trip_no_slash(token, user_id):
    print("\n" + "="*50)
    print("3. Testing POST /api/v1/trips (NO trailing slash)")
    print("="*50)
    try:
        trip_data = {
            "start_time": datetime.now().isoformat(),
            "end_time": datetime.now().isoformat(),
            "duration_minutes": 5,
            "distance_km": 2.5,
            "safety_score": 90,
            "user_id": user_id
        }
        
        headers = {"Content-Type": "application/json"}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        
        response = requests.post(f"{BASE_URL}/api/v1/trips", json=trip_data, headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code in [200, 201]:
            print(f"✅ SUCCESS: {response.json()}")
            return True
        else:
            print(f"❌ FAILED: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_create_trip_with_slash(token, user_id):
    print("\n" + "="*50)
    print("4. Testing POST /api/v1/trips/ (WITH trailing slash)")
    print("="*50)
    try:
        trip_data = {
            "start_time": datetime.now().isoformat(),
            "end_time": datetime.now().isoformat(),
            "duration_minutes": 5,
            "distance_km": 2.5,
            "safety_score": 90,
            "user_id": user_id
        }
        
        headers = {"Content-Type": "application/json"}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        
        response = requests.post(f"{BASE_URL}/api/v1/trips/", json=trip_data, headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code in [200, 201]:
            print(f"✅ SUCCESS: {response.json()}")
            return True
        else:
            print(f"❌ FAILED: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_get_trips_no_slash(token):
    print("\n" + "="*50)
    print("5. Testing GET /api/v1/trips (NO trailing slash)")
    print("="*50)
    try:
        headers = {}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        
        response = requests.get(f"{BASE_URL}/api/v1/trips", headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ SUCCESS: Got {len(data)} trips")
            return True
        else:
            print(f"❌ FAILED: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_get_trips_with_slash(token):
    print("\n" + "="*50)
    print("6. Testing GET /api/v1/trips/ (WITH trailing slash)")
    print("="*50)
    try:
        headers = {}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        
        response = requests.get(f"{BASE_URL}/api/v1/trips/", headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ SUCCESS: Got {len(data)} trips")
            return True
        else:
            print(f"❌ FAILED: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_create_alerts(token, user_id):
    print("\n" + "="*50)
    print("7. Testing POST /api/v1/alerts")
    print("="*50)
    try:
        alerts_data = [{
            "user_id": user_id,
            "alert_type": "test_alert",
            "severity": "medium",
            "timestamp": datetime.now().isoformat(),
            "message": "Test alert from script"
        }]
        
        headers = {"Content-Type": "application/json"}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        
        response = requests.post(f"{BASE_URL}/api/v1/alerts", json=alerts_data, headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code in [200, 201]:
            print(f"✅ SUCCESS: {response.json()}")
            return True
        else:
            print(f"❌ FAILED: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_get_alerts(token):
    print("\n" + "="*50)
    print("8. Testing GET /api/v1/alerts")
    print("="*50)
    try:
        headers = {}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        
        response = requests.get(f"{BASE_URL}/api/v1/alerts", headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ SUCCESS: Got {len(data)} alerts")
            return True
        else:
            print(f"❌ FAILED: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def check_redirect_behavior():
    print("\n" + "="*50)
    print("9. Checking Redirect Behavior")
    print("="*50)
    
    # Check if server has duplicate routes
    print("\nChecking POST /api/v1/trips (no slash):")
    try:
        response = requests.post(f"{BASE_URL}/api/v1/trips", json={})
        print(f"  Status: {response.status_code}")
        if 300 <= response.status_code < 400:
            print(f"  ⚠️ Redirects to: {response.headers.get('Location', 'Unknown')}")
    except:
        pass
    
    print("\nChecking POST /api/v1/trips/ (with slash):")
    try:
        response = requests.post(f"{BASE_URL}/api/v1/trips/", json={})
        print(f"  Status: {response.status_code}")
        if 300 <= response.status_code < 400:
            print(f"  ⚠️ Redirects to: {response.headers.get('Location', 'Unknown')}")
    except:
        pass

def main():
    print("🚀 Starting Backend Tests")
    print(f"Base URL: {BASE_URL}")
    
    # Test 1: Health
    if not test_health():
        print("\n❌ Server is not reachable! Check if server is running.")
        return
    
    # Test 2: Login
    token, user_id = test_login()
    if not token:
        print("\n⚠️ Login failed, continuing without token...")
    
    # Test 3 & 4: Check which endpoint works
    print("\n" + "="*50)
    print("🔍 IDENTIFYING THE PROBLEM")
    print("="*50)
    
    no_slash_works = test_create_trip_no_slash(token, user_id if user_id else 1)
    with_slash_works = test_create_trip_with_slash(token, user_id if user_id else 1)
    
    print("\n" + "="*50)
    print("📊 RESULTS:")
    print("="*50)
    
    if no_slash_works and not with_slash_works:
        print("✅ NO trailing slash works (correct)")
        print("❌ WITH trailing slash fails (redirect loop)")
        print("\n👉 FIX: Remove all trailing slashes from your Android code")
        print("   Change 'api/v1/trips/' to 'api/v1/trips'")
    elif not no_slash_works and with_slash_works:
        print("✅ WITH trailing slash works")
        print("❌ NO trailing slash fails")
        print("\n👉 FIX: Keep trailing slashes in your Android code")
        print("   Keep 'api/v1/trips/' as is")
    elif no_slash_works and with_slash_works:
        print("⚠️ BOTH endpoints work - You have duplicate routes!")
        print("\n👉 FIX: Remove duplicate routes from your FastAPI backend")
        print("   Keep ONLY ONE route (preferably without trailing slash)")
    else:
        print("❌ BOTH endpoints failed - Check your backend")
    
    # Test get endpoints
    test_get_trips_no_slash(token)
    test_get_trips_with_slash(token)
    
    # Test alerts
    test_create_alerts(token, user_id if user_id else 1)
    test_get_alerts(token)
    
    # Check redirect behavior
    check_redirect_behavior()
    
    print("\n" + "="*50)
    print("✅ Tests Complete!")
    print("="*50)

if __name__ == "__main__":
    main()