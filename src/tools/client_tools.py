from typing import Dict, Any, Optional, List
from ..common.server import mcp
from .keycloak_client import KeycloakClient


client = KeycloakClient()


@mcp.tool()
def list_clients(
    client_id: Optional[str] = None,
    viewable_only: bool = False,
    first: Optional[int] = None,
    max: Optional[int] = None
) -> List[Dict[str, Any]]:
    """
    List clients in the realm.
    
    Args:
        client_id: Filter by client ID (partial match)
        viewable_only: Only return viewable clients
        first: Pagination offset
        max: Maximum results size
        
    Returns:
        List of client objects
    """
    params = {}
    if client_id:
        params["clientId"] = client_id
    if viewable_only:
        params["viewableOnly"] = "true"
    if first is not None:
        params["first"] = first
    if max is not None:
        params["max"] = max
        
    return client._make_request("GET", "/clients", params=params)


@mcp.tool()
def get_client(id: str) -> Dict[str, Any]:
    """
    Get a specific client by database ID.
    
    Args:
        id: The client's database ID (not client_id)
        
    Returns:
        Client object
    """
    return client._make_request("GET", f"/clients/{id}")


@mcp.tool()
def get_client_by_clientid(client_id: str) -> Dict[str, Any]:
    """
    Get a specific client by client ID.
    
    Args:
        client_id: The client's client_id
        
    Returns:
        Client object
    """
    clients = client._make_request("GET", "/clients", params={"clientId": client_id})
    if clients and len(clients) > 0:
        # Find exact match
        for c in clients:
            if c.get("clientId") == client_id:
                return c
    raise Exception(f"Client with client_id '{client_id}' not found")


@mcp.tool()
def create_client(
    client_id: str,
    name: Optional[str] = None,
    description: Optional[str] = None,
    enabled: bool = True,
    always_display_in_console: bool = False,
    root_url: Optional[str] = None,
    redirect_uris: Optional[List[str]] = None,
    web_origins: Optional[List[str]] = None,
    protocol: str = "openid-connect",
    public_client: bool = False,
    bearer_only: bool = False,
    service_accounts_enabled: bool = False,
    authorization_services_enabled: bool = False,
    direct_access_grants_enabled: bool = False,
    implicit_flow_enabled: bool = False,
    standard_flow_enabled: bool = True
) -> Dict[str, str]:
    """
    Create a new client.
    
    Args:
        client_id: Client ID (unique identifier)
        name: Display name
        description: Client description
        enabled: Whether the client is enabled
        always_display_in_console: Always display in account console
        root_url: Root URL for relative URLs
        redirect_uris: Valid redirect URIs
        web_origins: Allowed CORS origins
        protocol: Protocol (openid-connect or saml)
        public_client: Public client (no secret)
        bearer_only: Bearer-only client
        service_accounts_enabled: Enable service accounts
        authorization_services_enabled: Enable authorization services
        direct_access_grants_enabled: Enable direct access grants (password flow)
        implicit_flow_enabled: Enable implicit flow
        standard_flow_enabled: Enable standard flow (authorization code)
        
    Returns:
        Status message
    """
    client_data = {
        "clientId": client_id,
        "enabled": enabled,
        "alwaysDisplayInConsole": always_display_in_console,
        "protocol": protocol,
        "publicClient": public_client,
        "bearerOnly": bearer_only,
        "serviceAccountsEnabled": service_accounts_enabled,
        "authorizationServicesEnabled": authorization_services_enabled,
        "directAccessGrantsEnabled": direct_access_grants_enabled,
        "implicitFlowEnabled": implicit_flow_enabled,
        "standardFlowEnabled": standard_flow_enabled
    }
    
    if name:
        client_data["name"] = name
    if description:
        client_data["description"] = description
    if root_url:
        client_data["rootUrl"] = root_url
    if redirect_uris:
        client_data["redirectUris"] = redirect_uris
    if web_origins:
        client_data["webOrigins"] = web_origins
    
    client._make_request("POST", "/clients", data=client_data)
    return {"status": "created", "message": f"Client {client_id} created successfully"}


@mcp.tool()
def update_client(
    id: str,
    client_id: Optional[str] = None,
    name: Optional[str] = None,
    description: Optional[str] = None,
    enabled: Optional[bool] = None,
    redirect_uris: Optional[List[str]] = None,
    web_origins: Optional[List[str]] = None,
    public_client: Optional[bool] = None,
    service_accounts_enabled: Optional[bool] = None,
    direct_access_grants_enabled: Optional[bool] = None
) -> Dict[str, str]:
    """
    Update an existing client.
    
    Args:
        id: The client's database ID
        client_id: New client ID
        name: New display name
        description: New description
        enabled: Whether the client is enabled
        redirect_uris: New redirect URIs
        web_origins: New CORS origins
        public_client: Whether client is public
        service_accounts_enabled: Enable service accounts
        direct_access_grants_enabled: Enable direct access grants
        
    Returns:
        Status message
    """
    # Get current client data
    current_client = client._make_request("GET", f"/clients/{id}")
    
    # Update only provided fields
    if client_id is not None:
        current_client["clientId"] = client_id
    if name is not None:
        current_client["name"] = name
    if description is not None:
        current_client["description"] = description
    if enabled is not None:
        current_client["enabled"] = enabled
    if redirect_uris is not None:
        current_client["redirectUris"] = redirect_uris
    if web_origins is not None:
        current_client["webOrigins"] = web_origins
    if public_client is not None:
        current_client["publicClient"] = public_client
    if service_accounts_enabled is not None:
        current_client["serviceAccountsEnabled"] = service_accounts_enabled
    if direct_access_grants_enabled is not None:
        current_client["directAccessGrantsEnabled"] = direct_access_grants_enabled
    
    client._make_request("PUT", f"/clients/{id}", data=current_client)
    return {"status": "updated", "message": f"Client {id} updated successfully"}


@mcp.tool()
def delete_client(id: str) -> Dict[str, str]:
    """
    Delete a client.
    
    Args:
        id: The client's database ID
        
    Returns:
        Status message
    """
    client._make_request("DELETE", f"/clients/{id}")
    return {"status": "deleted", "message": f"Client {id} deleted successfully"}


@mcp.tool()
def get_client_secret(id: str) -> Dict[str, str]:
    """
    Get the client secret.
    
    Args:
        id: The client's database ID
        
    Returns:
        Client secret object
    """
    return client._make_request("GET", f"/clients/{id}/client-secret")


@mcp.tool()
def regenerate_client_secret(id: str) -> Dict[str, str]:
    """
    Regenerate the client secret.
    
    Args:
        id: The client's database ID
        
    Returns:
        New client secret object
    """
    return client._make_request("POST", f"/clients/{id}/client-secret")


@mcp.tool()
def get_client_service_account(id: str) -> Dict[str, Any]:
    """
    Get service account user for a client.
    
    Args:
        id: The client's database ID
        
    Returns:
        Service account user object
    """
    return client._make_request("GET", f"/clients/{id}/service-account-user")