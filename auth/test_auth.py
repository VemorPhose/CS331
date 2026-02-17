"""
Test script for the Nexus Authentication API

This script demonstrates and tests the authentication system endpoints.
Run the FastAPI server first: python main.py
Then run this test script: python test_auth.py
"""

import requests
import json
from typing import Dict, Optional

# Configuration
BASE_URL = "http://localhost:8000"
TEST_EMAIL = "testuser@example.com"
TEST_PASSWORD = "TestPassword123!"


def print_response(response: requests.Response, title: str = "Response"):
    """Pretty print API response"""
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}")
    print(f"Status Code: {response.status_code}")
    try:
        print(json.dumps(response.json(), indent=2))
    except:
        print(f"Response: {response.text}")


def test_health_check():
    """Test the health check endpoint"""
    print("\n" + "="*60)
    print("TEST 1: Health Check")
    print("="*60)
    
    response = requests.get(f"{BASE_URL}/")
    print_response(response, "Health Check Response")
    
    return response.status_code == 200


def test_register():
    """Test user registration"""
    print("\n" + "="*60)
    print("TEST 2: User Registration")
    print("="*60)
    
    user_data = {
        "email": TEST_EMAIL,
        "password": TEST_PASSWORD
    }
    
    print(f"Registering user: {json.dumps(user_data, indent=2)}")
    
    response = requests.post(
        f"{BASE_URL}/register",
        json=user_data
    )
    print_response(response, "Registration Response")
    
    return response.status_code in [201, 400]  # 201 or 400 if already exists


def test_duplicate_registration():
    """Test registration with duplicate email"""
    print("\n" + "="*60)
    print("TEST 3: Duplicate Registration (Should Fail)")
    print("="*60)
    
    user_data = {
        "email": TEST_EMAIL,
        "password": TEST_PASSWORD
    }
    
    response = requests.post(
        f"{BASE_URL}/register",
        json=user_data
    )
    print_response(response, "Duplicate Registration Response")
    
    return response.status_code == 400


def test_login():
    """Test user login"""
    print("\n" + "="*60)
    print("TEST 4: User Login")
    print("="*60)
    
    login_data = {
        "email": TEST_EMAIL,
        "password": TEST_PASSWORD
    }
    
    print(f"Logging in user: {json.dumps(login_data, indent=2)}")
    
    response = requests.post(
        f"{BASE_URL}/login",
        json=login_data
    )
    print_response(response, "Login Response")
    
    if response.status_code == 200:
        return response.json().get("access_token")
    return None


def test_invalid_login():
    """Test login with invalid credentials"""
    print("\n" + "="*60)
    print("TEST 5: Invalid Login (Should Fail)")
    print("="*60)
    
    login_data = {
        "email": TEST_EMAIL,
        "password": "WrongPassword123!"
    }
    
    response = requests.post(
        f"{BASE_URL}/login",
        json=login_data
    )
    print_response(response, "Invalid Login Response")
    
    return response.status_code == 401


def test_get_current_user(token: str):
    """Test getting current user info"""
    print("\n" + "="*60)
    print("TEST 6: Get Current User Info")
    print("="*60)
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    response = requests.get(
        f"{BASE_URL}/me",
        headers=headers
    )
    print_response(response, "Current User Response")
    
    return response.status_code == 200


def test_unauthorized_access():
    """Test accessing protected route without token"""
    print("\n" + "="*60)
    print("TEST 7: Unauthorized Access (Should Fail)")
    print("="*60)
    
    response = requests.get(f"{BASE_URL}/me")
    print_response(response, "Unauthorized Access Response")
    
    return response.status_code == 403


def test_invalid_token():
    """Test accessing protected route with invalid token"""
    print("\n" + "="*60)
    print("TEST 8: Invalid Token (Should Fail)")
    print("="*60)
    
    headers = {
        "Authorization": "Bearer invalid_token_12345"
    }
    
    response = requests.get(
        f"{BASE_URL}/me",
        headers=headers
    )
    print_response(response, "Invalid Token Response")
    
    return response.status_code == 401


def test_oauth2_token_endpoint():
    """Test OAuth2 compatible token endpoint"""
    print("\n" + "="*60)
    print("TEST 9: OAuth2 Token Endpoint")
    print("="*60)
    
    form_data = {
        "username": TEST_EMAIL,
        "password": TEST_PASSWORD
    }
    
    print(f"Getting token via OAuth2 endpoint with: {json.dumps(form_data, indent=2)}")
    
    response = requests.post(
        f"{BASE_URL}/token",
        data=form_data
    )
    print_response(response, "OAuth2 Token Response")
    
    if response.status_code == 200:
        return response.json().get("access_token")
    return None


def run_all_tests():
    """Run all tests"""
    print("\n" + "="*80)
    print("NEXUS AUTHENTICATION SYSTEM - TEST SUITE")
    print("="*80)
    
    results = {}
    
    try:
        # Test 1: Health check
        results["Health Check"] = test_health_check()
        
        # Test 2: Registration
        results["User Registration"] = test_register()
        
        # Test 3: Duplicate registration
        results["Duplicate Registration"] = test_duplicate_registration()
        
        # Test 4: Login
        token = test_login()
        results["User Login"] = token is not None
        
        if token:
            # Test 5: Get current user
            results["Get Current User"] = test_get_current_user(token)
        
        # Test 6: Invalid login
        results["Invalid Login"] = test_invalid_login()
        
        # Test 7: Unauthorized access
        results["Unauthorized Access"] = test_unauthorized_access()
        
        # Test 8: Invalid token
        results["Invalid Token"] = test_invalid_token()
        
        # Test 9: OAuth2 token endpoint
        oauth2_token = test_oauth2_token_endpoint()
        results["OAuth2 Token Endpoint"] = oauth2_token is not None
        
        # Summary
        print("\n" + "="*80)
        print("TEST SUMMARY")
        print("="*80)
        
        passed = sum(1 for v in results.values() if v)
        total = len(results)
        
        for test_name, passed_flag in results.items():
            status = "✓ PASSED" if passed_flag else "✗ FAILED"
            print(f"{test_name:.<50} {status}")
        
        print("="*80)
        print(f"Total: {passed}/{total} tests passed")
        print("="*80)
        
    except requests.exceptions.ConnectionError:
        print("\n" + "="*80)
        print("ERROR: Could not connect to the API server")
        print("Please make sure the FastAPI server is running on http://localhost:8000")
        print("Run: python main.py")
        print("="*80)
    except Exception as e:
        print(f"\nUnexpected error: {e}")


if __name__ == "__main__":
    run_all_tests()
