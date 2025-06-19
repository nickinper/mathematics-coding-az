#!/usr/bin/env python3
"""
Simple test script for the execution API without authentication.
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

async def test_execution_direct():
    """Test the execution API directly."""
    async with httpx.AsyncClient() as client:
        # Test direct execution
        print("\nTesting direct execution...")
        try:
            response = await client.post(
                f"{BASE_URL}/api/execution/direct-execute",
                json=request_data
            )
            print(f"Status code: {response.status_code}")
            if response.status_code == 200:
                print(json.dumps(response.json(), indent=2))
            else:
                print(f"Error: {response.text}")
        except Exception as e:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_execution_direct())