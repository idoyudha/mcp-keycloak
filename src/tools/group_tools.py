from typing import Dict, Any, Optional, List
from ..common.server import mcp
from .keycloak_client import KeycloakClient


client = KeycloakClient()


@mcp.tool()
def list_groups(
    first: Optional[int] = None, max: Optional[int] = None, search: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    List all groups in the realm.

    Args:
        first: Pagination offset
        max: Maximum results size
        search: Search string

    Returns:
        List of groups
    """
    params = {}
    if first is not None:
        params["first"] = first
    if max is not None:
        params["max"] = max
    if search:
        params["search"] = search

    return client._make_request("GET", "/groups", params=params)


@mcp.tool()
def get_group(group_id: str) -> Dict[str, Any]:
    """
    Get a specific group by ID.

    Args:
        group_id: Group ID

    Returns:
        Group object
    """
    return client._make_request("GET", f"/groups/{group_id}")


@mcp.tool()
def create_group(
    name: str,
    path: Optional[str] = None,
    attributes: Optional[Dict[str, List[str]]] = None,
) -> Dict[str, str]:
    """
    Create a new group.

    Args:
        name: Group name
        path: Group path
        attributes: Group attributes

    Returns:
        Status message
    """
    group_data = {"name": name}

    if path:
        group_data["path"] = path
    if attributes:
        group_data["attributes"] = attributes

    client._make_request("POST", "/groups", data=group_data)
    return {"status": "created", "message": f"Group {name} created successfully"}


@mcp.tool()
def update_group(
    group_id: str,
    name: Optional[str] = None,
    path: Optional[str] = None,
    attributes: Optional[Dict[str, List[str]]] = None,
) -> Dict[str, str]:
    """
    Update a group.

    Args:
        group_id: Group ID
        name: New group name
        path: New group path
        attributes: New group attributes

    Returns:
        Status message
    """
    # Get current group
    current_group = client._make_request("GET", f"/groups/{group_id}")

    # Update only provided fields
    if name is not None:
        current_group["name"] = name
    if path is not None:
        current_group["path"] = path
    if attributes is not None:
        current_group["attributes"] = attributes

    client._make_request("PUT", f"/groups/{group_id}", data=current_group)
    return {"status": "updated", "message": f"Group {group_id} updated successfully"}


@mcp.tool()
def delete_group(group_id: str) -> Dict[str, str]:
    """
    Delete a group.

    Args:
        group_id: Group ID

    Returns:
        Status message
    """
    client._make_request("DELETE", f"/groups/{group_id}")
    return {"status": "deleted", "message": f"Group {group_id} deleted successfully"}


@mcp.tool()
def get_group_members(
    group_id: str, first: Optional[int] = None, max: Optional[int] = None
) -> List[Dict[str, Any]]:
    """
    Get members of a group.

    Args:
        group_id: Group ID
        first: Pagination offset
        max: Maximum results size

    Returns:
        List of group members
    """
    params = {}
    if first is not None:
        params["first"] = first
    if max is not None:
        params["max"] = max

    return client._make_request("GET", f"/groups/{group_id}/members", params=params)


@mcp.tool()
def add_user_to_group(user_id: str, group_id: str) -> Dict[str, str]:
    """
    Add a user to a group.

    Args:
        user_id: User ID
        group_id: Group ID

    Returns:
        Status message
    """
    client._make_request("PUT", f"/users/{user_id}/groups/{group_id}")
    return {"status": "added", "message": f"User {user_id} added to group {group_id}"}


@mcp.tool()
def remove_user_from_group(user_id: str, group_id: str) -> Dict[str, str]:
    """
    Remove a user from a group.

    Args:
        user_id: User ID
        group_id: Group ID

    Returns:
        Status message
    """
    client._make_request("DELETE", f"/users/{user_id}/groups/{group_id}")
    return {
        "status": "removed",
        "message": f"User {user_id} removed from group {group_id}",
    }


@mcp.tool()
def get_user_groups(user_id: str) -> List[Dict[str, Any]]:
    """
    Get all groups for a user.

    Args:
        user_id: User ID

    Returns:
        List of groups the user belongs to
    """
    return client._make_request("GET", f"/users/{user_id}/groups")
