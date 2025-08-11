from typing import Dict, Any, Optional, List
from ..common.server import mcp
from .keycloak_client import KeycloakClient


client = KeycloakClient()


@mcp.tool()
async def list_realm_roles(
    first: Optional[int] = None,
    max: Optional[int] = None,
    search: Optional[str] = None,
    realm: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    List all realm roles.

    Args:
        first: Pagination offset
        max: Maximum results size
        search: Search string
        realm: Target realm (uses default if not specified)

    Returns:
        List of realm roles
    """
    params = {}
    if first is not None:
        params["first"] = first
    if max is not None:
        params["max"] = max
    if search:
        params["search"] = search

    return await client._make_request("GET", "/roles", params=params, realm=realm)


@mcp.tool()
async def get_realm_role(role_name: str, realm: Optional[str] = None) -> Dict[str, Any]:
    """
    Get a specific realm role by name.

    Args:
        role_name: Role name
        realm: Target realm (uses default if not specified)

    Returns:
        Role object
    """
    return await client._make_request("GET", f"/roles/{role_name}", realm=realm)


@mcp.tool()
async def create_realm_role(
    name: str,
    description: Optional[str] = None,
    composite: bool = False,
    client_role: bool = False,
    realm: Optional[str] = None,
) -> Dict[str, str]:
    """
    Create a new realm role.

    Args:
        name: Role name
        description: Role description
        composite: Whether this is a composite role
        client_role: Whether this is a client role
        realm: Target realm (uses default if not specified)

    Returns:
        Status message
    """
    role_data = {"name": name, "composite": composite, "clientRole": client_role}

    if description:
        role_data["description"] = description

    await client._make_request("POST", "/roles", data=role_data, realm=realm)
    return {"status": "created", "message": f"Realm role {name} created successfully"}


@mcp.tool()
async def update_realm_role(
    role_name: str,
    description: Optional[str] = None,
    composite: Optional[bool] = None,
    realm: Optional[str] = None,
) -> Dict[str, str]:
    """
    Update a realm role.

    Args:
        role_name: Current role name
        description: New description
        composite: Whether this is a composite role
        realm: Target realm (uses default if not specified)

    Returns:
        Status message
    """
    # Get current role
    current_role = await client._make_request("GET", f"/roles/{role_name}", realm=realm)

    # Update only provided fields
    if description is not None:
        current_role["description"] = description
    if composite is not None:
        current_role["composite"] = composite

    await client._make_request(
        "PUT", f"/roles/{role_name}", data=current_role, realm=realm
    )
    return {
        "status": "updated",
        "message": f"Realm role {role_name} updated successfully",
    }


@mcp.tool()
async def delete_realm_role(
    role_name: str, realm: Optional[str] = None
) -> Dict[str, str]:
    """
    Delete a realm role.

    Args:
        role_name: Role name to delete
        realm: Target realm (uses default if not specified)

    Returns:
        Status message
    """
    await client._make_request("DELETE", f"/roles/{role_name}", realm=realm)
    return {
        "status": "deleted",
        "message": f"Realm role {role_name} deleted successfully",
    }


@mcp.tool()
async def list_client_roles(
    client_id: str,
    first: Optional[int] = None,
    max: Optional[int] = None,
    search: Optional[str] = None,
    realm: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    List roles for a specific client.

    Args:
        client_id: Client database ID
        first: Pagination offset
        max: Maximum results size
        search: Search string
        realm: Target realm (uses default if not specified)

    Returns:
        List of client roles
    """
    params = {}
    if first is not None:
        params["first"] = first
    if max is not None:
        params["max"] = max
    if search:
        params["search"] = search

    return await client._make_request(
        "GET", f"/clients/{client_id}/roles", params=params, realm=realm
    )


@mcp.tool()
async def create_client_role(
    client_id: str,
    name: str,
    description: Optional[str] = None,
    composite: bool = False,
    realm: Optional[str] = None,
) -> Dict[str, str]:
    """
    Create a new client role.

    Args:
        client_id: Client database ID
        name: Role name
        description: Role description
        composite: Whether this is a composite role
        realm: Target realm (uses default if not specified)

    Returns:
        Status message
    """
    role_data = {"name": name, "composite": composite, "clientRole": True}

    if description:
        role_data["description"] = description

    await client._make_request(
        "POST", f"/clients/{client_id}/roles", data=role_data, realm=realm
    )
    return {"status": "created", "message": f"Client role {name} created successfully"}


@mcp.tool()
async def assign_realm_role_to_user(
    user_id: str, role_names: List[str], realm: Optional[str] = None
) -> Dict[str, str]:
    """
    Assign realm roles to a user.

    Args:
        user_id: User ID
        role_names: List of role names to assign
        realm: Target realm (uses default if not specified)

    Returns:
        Status message
    """
    # Get role representations
    roles = []
    for role_name in role_names:
        role = await client._make_request("GET", f"/roles/{role_name}", realm=realm)
        roles.append(role)

    await client._make_request(
        "POST", f"/users/{user_id}/role-mappings/realm", data=roles, realm=realm
    )
    return {
        "status": "assigned",
        "message": f"Roles {role_names} assigned to user {user_id}",
    }


@mcp.tool()
async def remove_realm_role_from_user(
    user_id: str, role_names: List[str], realm: Optional[str] = None
) -> Dict[str, str]:
    """
    Remove realm roles from a user.

    Args:
        user_id: User ID
        role_names: List of role names to remove
        realm: Target realm (uses default if not specified)

    Returns:
        Status message
    """
    # Get role representations
    roles = []
    for role_name in role_names:
        role = await client._make_request("GET", f"/roles/{role_name}", realm=realm)
        roles.append(role)

    await client._make_request(
        "DELETE", f"/users/{user_id}/role-mappings/realm", data=roles, realm=realm
    )
    return {
        "status": "removed",
        "message": f"Roles {role_names} removed from user {user_id}",
    }


@mcp.tool()
async def get_user_realm_roles(
    user_id: str, effective: bool = False, realm: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Get realm roles for a user.

    Args:
        user_id: User ID
        effective: Get effective roles (including composite roles)
        realm: Target realm (uses default if not specified)

    Returns:
        List of realm roles
    """
    endpoint = f"/users/{user_id}/role-mappings/realm"
    if effective:
        endpoint += "/composite"

    return await client._make_request("GET", endpoint, realm=realm)


@mcp.tool()
async def assign_client_role_to_user(
    user_id: str, client_id: str, role_names: List[str], realm: Optional[str] = None
) -> Dict[str, str]:
    """
    Assign client roles to a user.

    Args:
        user_id: User ID
        client_id: Client database ID
        role_names: List of role names to assign
        realm: Target realm (uses default if not specified)

    Returns:
        Status message
    """
    # Get role representations
    roles = []
    for role_name in role_names:
        role = await client._make_request(
            "GET", f"/clients/{client_id}/roles/{role_name}", realm=realm
        )
        roles.append(role)

    await client._make_request(
        "POST",
        f"/users/{user_id}/role-mappings/clients/{client_id}",
        data=roles,
        realm=realm,
    )
    return {
        "status": "assigned",
        "message": f"Client roles {role_names} assigned to user {user_id}",
    }
