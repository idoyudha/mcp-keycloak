from typing import Dict, Any, Optional, List
from ..common.server import mcp
from .keycloak_client import KeycloakClient


client = KeycloakClient()


@mcp.tool()
async def list_groups(
    first: Optional[int] = None,
    max: Optional[int] = None,
    search: Optional[str] = None,
    realm: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    List all groups in the realm.

    Args:
        first: Pagination offset
        max: Maximum results size
        search: Search string
        realm: Target realm (uses default if not specified)

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

    return await client._make_request("GET", "/groups", params=params, realm=realm)


@mcp.tool()
async def get_group(group_id: str, realm: Optional[str] = None) -> Dict[str, Any]:
    """
    Get a specific group by ID.

    Args:
        group_id: Group ID
        realm: Target realm (uses default if not specified)

    Returns:
        Group object
    """
    return await client._make_request("GET", f"/groups/{group_id}", realm=realm)


@mcp.tool()
async def create_group(
    name: str,
    path: Optional[str] = None,
    attributes: Optional[Dict[str, List[str]]] = None,
    realm: Optional[str] = None,
) -> Dict[str, str]:
    """
    Create a new group.

    Args:
        name: Group name
        path: Group path
        attributes: Group attributes
        realm: Target realm (uses default if not specified)

    Returns:
        Status message
    """
    group_data = {"name": name}

    if path:
        group_data["path"] = path
    if attributes:
        group_data["attributes"] = attributes

    await client._make_request("POST", "/groups", data=group_data, realm=realm)
    return {"status": "created", "message": f"Group {name} created successfully"}


@mcp.tool()
async def update_group(
    group_id: str,
    name: Optional[str] = None,
    path: Optional[str] = None,
    attributes: Optional[Dict[str, List[str]]] = None,
    realm: Optional[str] = None,
) -> Dict[str, str]:
    """
    Update a group.

    Args:
        group_id: Group ID
        name: New group name
        path: New group path
        attributes: New group attributes
        realm: Target realm (uses default if not specified)

    Returns:
        Status message
    """
    # Get current group
    current_group = await client._make_request(
        "GET", f"/groups/{group_id}", realm=realm
    )

    # Update only provided fields
    if name is not None:
        current_group["name"] = name
    if path is not None:
        current_group["path"] = path
    if attributes is not None:
        current_group["attributes"] = attributes

    await client._make_request(
        "PUT", f"/groups/{group_id}", data=current_group, realm=realm
    )
    return {"status": "updated", "message": f"Group {group_id} updated successfully"}


@mcp.tool()
async def delete_group(group_id: str, realm: Optional[str] = None) -> Dict[str, str]:
    """
    Delete a group.

    Args:
        group_id: Group ID
        realm: Target realm (uses default if not specified)

    Returns:
        Status message
    """
    await client._make_request("DELETE", f"/groups/{group_id}", realm=realm)
    return {"status": "deleted", "message": f"Group {group_id} deleted successfully"}


@mcp.tool()
async def get_group_members(
    group_id: str,
    first: Optional[int] = None,
    max: Optional[int] = None,
    realm: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Get members of a group.

    Args:
        group_id: Group ID
        first: Pagination offset
        max: Maximum results size
        realm: Target realm (uses default if not specified)

    Returns:
        List of group members
    """
    params = {}
    if first is not None:
        params["first"] = first
    if max is not None:
        params["max"] = max

    return await client._make_request(
        "GET", f"/groups/{group_id}/members", params=params, realm=realm
    )


@mcp.tool()
async def add_user_to_group(
    user_id: str, group_id: str, realm: Optional[str] = None
) -> Dict[str, str]:
    """
    Add a user to a group.

    Args:
        user_id: User ID
        group_id: Group ID
        realm: Target realm (uses default if not specified)

    Returns:
        Status message
    """
    await client._make_request(
        "PUT", f"/users/{user_id}/groups/{group_id}", realm=realm
    )
    return {"status": "added", "message": f"User {user_id} added to group {group_id}"}


@mcp.tool()
async def remove_user_from_group(
    user_id: str, group_id: str, realm: Optional[str] = None
) -> Dict[str, str]:
    """
    Remove a user from a group.

    Args:
        user_id: User ID
        group_id: Group ID
        realm: Target realm (uses default if not specified)

    Returns:
        Status message
    """
    await client._make_request(
        "DELETE", f"/users/{user_id}/groups/{group_id}", realm=realm
    )
    return {
        "status": "removed",
        "message": f"User {user_id} removed from group {group_id}",
    }


@mcp.tool()
async def get_user_groups(
    user_id: str, realm: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Get all groups for a user.

    Args:
        user_id: User ID
        realm: Target realm (uses default if not specified)

    Returns:
        List of groups the user belongs to
    """
    return await client._make_request("GET", f"/users/{user_id}/groups", realm=realm)
