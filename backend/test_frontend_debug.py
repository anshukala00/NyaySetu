"""Debug script to test what the frontend should be receiving"""
import requests
import json

BASE_URL = "http://localhost:8000/api"

# Login as citizen
print("Logging in as citizen...")
response = requests.post(f"{BASE_URL}/auth/login", json={
    "email": "citizen1@example.com",
    "password": "password123"
})

if response.status_code == 200:
    data = response.json()
    token = data["access_token"]
    user_id = data["user_id"]
    role = data["role"]
    
    print(f"✓ Login successful")
    print(f"  User ID: {user_id}")
    print(f"  Role: {role}")
    print(f"  Token: {token[:30]}...")
    
    # Fetch cases
    print("\nFetching cases...")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/cases", headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Cases fetched successfully")
        print(f"  Response structure: {json.dumps(data, indent=2, default=str)[:500]}...")
        print(f"\n  Total: {data['total']}")
        print(f"  Page: {data['page']}")
        print(f"  Limit: {data['limit']}")
        print(f"  Cases array length: {len(data['cases'])}")
        
        if data['cases']:
            print(f"\n  First case:")
            case = data['cases'][0]
            print(f"    ID: {case['id']}")
            print(f"    Title: {case['title']}")
            print(f"    Status: {case['status']}")
            print(f"    Priority: {case.get('priority', 'None')}")
    else:
        print(f"✗ Failed to fetch cases: {response.status_code}")
        print(f"  Error: {response.text}")
else:
    print(f"✗ Login failed: {response.status_code}")
    print(f"  Error: {response.text}")
