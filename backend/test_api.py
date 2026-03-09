"""Quick test to verify API endpoints are working"""
import requests
import json

BASE_URL = "http://localhost:8000/api"

# Test 1: Login as judge
print("=" * 60)
print("TEST 1: Login as judge")
print("=" * 60)
try:
    response = requests.post(f"{BASE_URL}/auth/login", json={
        "email": "judge1@example.com",
        "password": "password123"
    })
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        token = data.get("access_token")
        print(f"Token: {token[:50]}...")
        
        # Test 2: Fetch cases as judge
        print("\n" + "=" * 60)
        print("TEST 2: Fetch cases as judge")
        print("=" * 60)
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{BASE_URL}/cases", headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Response keys: {data.keys()}")
            print(f"Total cases: {data.get('total', 0)}")
            print(f"Cases count: {len(data.get('cases', []))}")
            if data.get('cases'):
                print(f"First case: {data['cases'][0]['title']}")
        else:
            print(f"Error: {response.text}")
    else:
        print(f"Error: {response.text}")
except Exception as e:
    print(f"Error: {e}")

# Test 3: Login as citizen
print("\n" + "=" * 60)
print("TEST 3: Login as citizen")
print("=" * 60)
try:
    response = requests.post(f"{BASE_URL}/auth/login", json={
        "email": "citizen1@example.com",
        "password": "password123"
    })
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        token = data.get("access_token")
        print(f"Token: {token[:50]}...")
        
        # Test 4: Fetch cases as citizen
        print("\n" + "=" * 60)
        print("TEST 4: Fetch cases as citizen")
        print("=" * 60)
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{BASE_URL}/cases", headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Response keys: {data.keys()}")
            print(f"Total cases: {data.get('total', 0)}")
            print(f"Cases count: {len(data.get('cases', []))}")
            if data.get('cases'):
                print(f"First case: {data['cases'][0]['title']}")
        else:
            print(f"Error: {response.text}")
    else:
        print(f"Error: {response.text}")
except Exception as e:
    print(f"Error: {e}")
