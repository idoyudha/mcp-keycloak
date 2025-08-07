"""Basic import tests that don't require Keycloak connection"""

import pytest


def test_can_import_main():
    """Test that we can import the main module"""
    from src.main import KeycloakMCPServer, main
    assert KeycloakMCPServer is not None
    assert main is not None


def test_can_import_tools():
    """Test that we can import all tool modules"""
    from src.tools import user_tools
    from src.tools import client_tools
    from src.tools import realm_tools
    from src.tools import role_tools
    from src.tools import group_tools
    
    # Just check they imported successfully
    assert user_tools is not None
    assert client_tools is not None
    assert realm_tools is not None
    assert role_tools is not None
    assert group_tools is not None


def test_can_import_keycloak_client():
    """Test that we can import the Keycloak client"""
    from src.tools.keycloak_client import KeycloakClient
    assert KeycloakClient is not None


def test_can_import_config():
    """Test that we can import the config module"""
    from src.common.config import Config
    assert Config is not None


def test_can_import_server():
    """Test that we can import the server module"""
    from src.common.server import mcp
    assert mcp is not None