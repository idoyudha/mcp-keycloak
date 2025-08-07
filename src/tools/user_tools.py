from typing import Dict, Any, Optional, List
from ..common.server import mcp
from .keycloak_client import KeycloakClient


client = KeycloakClient()


@mcp.tool()
def list_users(
    first: Optional[int] = None,
    max: Optional[int] = None,
    search: Optional[str] = None,
    username: Optional[str] = None,
    email: Optional[str] = None,
    enabled: Optional[bool] = None,
) -> List[Dict[str, Any]]:
    """
    List users in the realm.

    Args:
        first: Pagination offset
        max: Maximum results size (defaults to 100)
        search: Search string for username, first/last name, or email
        username: Username filter
        email: Email filter
        enabled: Filter by enabled/disabled users

    Returns:
        List of user objects
    """
    params = {}
    if first is not None:
        params["first"] = first
    if max is not None:
        params["max"] = max
    if search:
        params["search"] = search
    if username:
        params["username"] = username
    if email:
        params["email"] = email
    if enabled is not None:
        params["enabled"] = str(enabled).lower()

    return client._make_request("GET", "/users", params=params)


@mcp.tool()
def get_user(user_id: str) -> Dict[str, Any]:
    """
    Get a specific user by ID.

    Args:
        user_id: The user's ID

    Returns:
        User object
    """
    return client._make_request("GET", f"/users/{user_id}")


@mcp.tool()
def create_user(
    username: str,
    email: Optional[str] = None,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    enabled: bool = True,
    email_verified: bool = False,
    temporary_password: Optional[str] = None,
    attributes: Optional[Dict[str, List[str]]] = None,
) -> Dict[str, str]:
    """
    Create a new user.

    Args:
        username: Username for the new user
        email: Email address
        first_name: First name
        last_name: Last name
        enabled: Whether the user is enabled
        email_verified: Whether the email is verified
        temporary_password: Initial password (user will be required to change it)
        attributes: Additional user attributes

    Returns:
        Dict with status and location of created user
    """
    user_data = {
        "username": username,
        "enabled": enabled,
        "emailVerified": email_verified,
    }

    if email:
        user_data["email"] = email
    if first_name:
        user_data["firstName"] = first_name
    if last_name:
        user_data["lastName"] = last_name
    if attributes:
        user_data["attributes"] = attributes

    if temporary_password:
        user_data["credentials"] = [
            {"type": "password", "value": temporary_password, "temporary": True}
        ]

    # Create user returns no content, but includes Location header
    client._make_request("POST", "/users", data=user_data)
    return {"status": "created", "message": f"User {username} created successfully"}


@mcp.tool()
def update_user(
    user_id: str,
    username: Optional[str] = None,
    email: Optional[str] = None,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    enabled: Optional[bool] = None,
    email_verified: Optional[bool] = None,
    attributes: Optional[Dict[str, List[str]]] = None,
) -> Dict[str, str]:
    """
    Update an existing user.

    Args:
        user_id: The user's ID
        username: New username
        email: New email address
        first_name: New first name
        last_name: New last name
        enabled: Whether the user is enabled
        email_verified: Whether the email is verified
        attributes: Updated user attributes

    Returns:
        Status message
    """
    # First get the current user data
    current_user = client._make_request("GET", f"/users/{user_id}")

    # Update only provided fields
    if username is not None:
        current_user["username"] = username
    if email is not None:
        current_user["email"] = email
    if first_name is not None:
        current_user["firstName"] = first_name
    if last_name is not None:
        current_user["lastName"] = last_name
    if enabled is not None:
        current_user["enabled"] = enabled
    if email_verified is not None:
        current_user["emailVerified"] = email_verified
    if attributes is not None:
        current_user["attributes"] = attributes

    client._make_request("PUT", f"/users/{user_id}", data=current_user)
    return {"status": "updated", "message": f"User {user_id} updated successfully"}


@mcp.tool()
def delete_user(user_id: str) -> Dict[str, str]:
    """
    Delete a user.

    Args:
        user_id: The user's ID

    Returns:
        Status message
    """
    client._make_request("DELETE", f"/users/{user_id}")
    return {"status": "deleted", "message": f"User {user_id} deleted successfully"}


@mcp.tool()
def reset_user_password(
    user_id: str, password: str, temporary: bool = True
) -> Dict[str, str]:
    """
    Reset a user's password.

    Args:
        user_id: The user's ID
        password: New password
        temporary: Whether the password is temporary (user must change on next login)

    Returns:
        Status message
    """
    credential_data = {"type": "password", "value": password, "temporary": temporary}

    client._make_request(
        "PUT", f"/users/{user_id}/reset-password", data=credential_data
    )
    return {"status": "success", "message": f"Password reset for user {user_id}"}


@mcp.tool()
def get_user_sessions(user_id: str) -> List[Dict[str, Any]]:
    """
    Get active sessions for a user.

    Args:
        user_id: The user's ID

    Returns:
        List of active sessions
    """
    return client._make_request("GET", f"/users/{user_id}/sessions")


@mcp.tool()
def logout_user(user_id: str) -> Dict[str, str]:
    """
    Logout all sessions for a user.

    Args:
        user_id: The user's ID

    Returns:
        Status message
    """
    client._make_request("POST", f"/users/{user_id}/logout")
    return {
        "status": "success",
        "message": f"User {user_id} logged out from all sessions",
    }


@mcp.tool()
def count_users() -> int:
    """
    Count all users.

    Returns:
        Number of users
    """
    return client._make_request("GET", "/users/count")
