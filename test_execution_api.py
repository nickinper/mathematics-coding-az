#!/usr/bin/env python3
"""
Simple test script for the execution API.
"""

import asyncio
import httpx
import json
import sys

# Base URL
BASE_URL = "http://localhost:8000"

# Test code
test_code = """
def add(a, b):
    return a + b
"""

# Test cases
test_cases = [
    {
        "function": "add",
        "input": {"a": 2, "b": 3},
        "expected_output": 5
    },
    {
        "function": "add",
        "input": {"a": -1, "b": 1},
        "expected_output": 0
    }
]

# Request data
request_data = {
    "code": test_code,
    "test_cases": test_cases,
    "language": "python"
}

async def register_and_login():
    """Register a test user and login."""
    async with httpx.AsyncClient() as client:
        # First, try to register a test user
        register_data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "password123",
            "full_name": "Test User"
        }
        
        try:
            print("Registering test user...")
            response = await client.post(
                f"{BASE_URL}/api/auth/register",
                json=register_data
            )
            
            if response.status_code == 200:
                print("User registered successfully")
                auth_data = response.json()
                return auth_data["token"]
            elif response.status_code == 400 and "already registered" in response.json().get("detail", ""):
                print("User already exists, trying to login...")
            else:
                print(f"Registration failed: {response.status_code}")
                print(json.dumps(response.json(), indent=2))
                return None
        except Exception as e:
            print(f"Registration error: {str(e)}")
        
        # Try to login
        try:
            print("Logging in...")
            response = await client.post(
                f"{BASE_URL}/api/auth/login",
                data={
                    "username": "testuser@example.com",
                    "password": "password123"
                },
                headers={"Content-Type": "application/x-www-form-urlencoded"}
            )
            
            if response.status_code == 200:
                print("Login successful")
                auth_data = response.json()
                return auth_data["token"]
            else:
                print(f"Login failed: {response.status_code}")
                print(json.dumps(response.json(), indent=2))
                return None
        except Exception as e:
            print(f"Login error: {str(e)}")
            return None

async def test_execution_api():
    """Test the execution API."""
    # Get authentication token
    token = await register_and_login()
    if not token:
        print("Failed to get authentication token. Exiting.")
        sys.exit(1)
    
    # Set authorization header
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    async with httpx.AsyncClient() as client:
        # Test /api/execution/execute endpoint
        print("\nTesting /api/execution/execute endpoint...")
        try:
            response = await client.post(
                f"{BASE_URL}/api/execution/execute",
                json=request_data,
                headers=headers
            )
            print(f"Status code: {response.status_code}")
            print(json.dumps(response.json(), indent=2))
        except Exception as e:
            print(f"Error: {str(e)}")
        
        # Test /api/execution/validate endpoint
        print("\nTesting /api/execution/validate endpoint...")
        try:
            response = await client.post(
                f"{BASE_URL}/api/execution/validate",
                json=request_data,
                headers=headers
            )
            print(f"Status code: {response.status_code}")
            print(json.dumps(response.json(), indent=2))
        except Exception as e:
            print(f"Error: {str(e)}")
        
        # Test /api/execution/metrics endpoint
        print("\nTesting /api/execution/metrics endpoint...")
        try:
            response = await client.get(
                f"{BASE_URL}/api/execution/metrics",
                headers=headers
            )
            print(f"Status code: {response.status_code}")
            print(json.dumps(response.json(), indent=2))
        except Exception as e:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_execution_api())