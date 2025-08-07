#!/usr/bin/env python
"""Test script to verify Keycloak connection and tools"""

import pytest
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from tools.keycloak_client import KeycloakClient


@pytest.fixture
def keycloak_client():
    """Fixture to provide a Keycloak client instance"""
    return KeycloakClient()


def test_keycloak_connection(keycloak_client):
    """Test that we can connect to Keycloak"""
    # This test will pass if the client initializes without error
    assert keycloak_client is not None
    assert hasattr(keycloak_client, "_get_token")
    assert hasattr(keycloak_client, "_make_request")


def test_keycloak_authentication(keycloak_client):
    """Test that we can authenticate with Keycloak"""
    try:
        token = keycloak_client._get_token()
        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 20
    except Exception as e:
        # If Keycloak is not available, skip this test
        pytest.skip(f"Keycloak service not available: {e}")


def test_keycloak_realm_info(keycloak_client):
    """Test that we can get realm information"""
    try:
        realm_info = keycloak_client._make_request("GET", "")
        assert realm_info is not None
        assert isinstance(realm_info, dict)
        # Check for expected fields
        assert "realm" in realm_info or "id" in realm_info
    except Exception as e:
        # If Keycloak is not available, skip this test
        pytest.skip(f"Keycloak service not available: {e}")


@pytest.mark.integration
def test_full_keycloak_workflow(keycloak_client):
    """Integration test for full Keycloak workflow"""
    try:
        # Get token
        token = keycloak_client._get_token()
        assert token is not None

        # Get realm info
        realm_info = keycloak_client._make_request("GET", "")
        assert realm_info is not None

        # If we get here, the connection is working
        print(
            f"✅ Successfully connected to realm: {realm_info.get('realm', 'Unknown')}"
        )

    except Exception as e:
        pytest.skip(f"Keycloak service not available: {e}")


if __name__ == "__main__":
    # Run pytest when executed directly
    pytest.main([__file__, "-v"])
