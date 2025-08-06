#!/usr/bin/env python
"""Test script to verify Keycloak connection and tools"""

import sys
sys.path.append('src')
from tools.keycloak_client import KeycloakClient

def test_connection():
    """Test the Keycloak connection"""
    try:
        client = KeycloakClient()
        print("Keycloak client initialized successfully")
        
        # Try to get a token
        token = client._get_token()
        print(f"Successfully authenticated! Token: {token[:20]}...")
        
        # Try to get realm info
        realm_info = client._make_request("GET", "")
        print(f"Connected to realm: {realm_info.get('realm', 'Unknown')}")
        print(f"Realm display name: {realm_info.get('displayName', 'Not set')}")
        
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    print("Testing Keycloak connection...")
    if test_connection():
        print("\n✅ Connection test passed!")
    else:
        print("\n❌ Connection test failed!")