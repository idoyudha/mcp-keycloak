from typing import Dict, Any, Optional, List
from ..common.server import mcp
from .keycloak_client import KeycloakClient


client = KeycloakClient()


# Flow Management Tools


@mcp.tool()
async def list_authentication_flows(
    realm: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Get authentication flows in the realm.

    Args:
        realm: Target realm (uses default if not specified)

    Returns:
        List of authentication flow objects
    """
    return await client._make_request("GET", "/authentication/flows", realm=realm)


@mcp.tool()
async def get_authentication_flow(
    flow_id: str,
    realm: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Get a specific authentication flow by ID.

    Args:
        flow_id: The flow's ID
        realm: Target realm (uses default if not specified)

    Returns:
        Authentication flow object
    """
    return await client._make_request(
        "GET", f"/authentication/flows/{flow_id}", realm=realm
    )


@mcp.tool()
async def create_authentication_flow(
    alias: str,
    description: str,
    id: Optional[str] = None,
    provider_id: str = "basic-flow",
    top_level: bool = True,
    built_in: bool = False,
    realm: Optional[str] = None,
) -> Dict[str, str]:
    """
    Create a new authentication flow.

    Args:
        alias: The flow's alias
        description: Flow description
        id: Flow ID
        provider_id: Provider ID (default: "basic-flow")
        top_level: Whether it's a top-level flow (default: True)
        built_in: Whether it's built-in (default: False)
        realm: Target realm (uses default if not specified)

    Returns:
        Status message
    """
    flow_data = {
        "alias": alias,
        "description": description,
        "providerId": provider_id,
        "topLevel": top_level,
        "builtIn": built_in,
    }

    if id is not None:
        flow_data["id"] = id

    await client._make_request(
        "POST", "/authentication/flows", data=flow_data, realm=realm
    )
    return {"status": f"Authentication flow '{alias}' created successfully"}


@mcp.tool()
async def delete_authentication_flow(
    flow_id: str,
    realm: Optional[str] = None,
) -> Dict[str, str]:
    """
    Delete an authentication flow.

    Args:
        flow_id: The flow's ID
        realm: Target realm (uses default if not specified)

    Returns:
        Status message
    """
    await client._make_request(
        "DELETE", f"/authentication/flows/{flow_id}", realm=realm
    )
    return {"status": f"Authentication flow deleted successfully"}


@mcp.tool()
async def update_authentication_flow(
    flow_id: str,
    alias: str,
    id: Optional[str] = None,
    description: Optional[str] = None,
    provider_id: Optional[str] = None,
    top_level: Optional[bool] = None,
    built_in: Optional[bool] = None,
    realm: Optional[str] = None,
) -> Dict[str, str]:
    """
    Update an authentication flow.

    Args:
        flow_id: The flow's ID (used in URL path)
        alias: The flow's alias
        id: Flow ID (for request body)
        description: Flow description
        provider_id: Provider ID
        top_level: Whether it's a top-level flow
        built_in: Whether it's built-in
        realm: Target realm (uses default if not specified)

    Returns:
        Status message
    """
    flow_data = {"alias": alias}

    if id is not None:
        flow_data["id"] = id
    if description is not None:
        flow_data["description"] = description
    if provider_id is not None:
        flow_data["providerId"] = provider_id
    if top_level is not None:
        flow_data["topLevel"] = top_level
    if built_in is not None:
        flow_data["builtIn"] = built_in

    await client._make_request(
        "PUT", f"/authentication/flows/{flow_id}", data=flow_data, realm=realm
    )
    return {"status": f"Authentication flow '{alias}' updated successfully"}


@mcp.tool()
async def copy_authentication_flow(
    flow_alias: str,
    new_name: str,
    realm: Optional[str] = None,
) -> Dict[str, str]:
    """
    Copy an existing authentication flow under a new name.

    Args:
        flow_alias: The source flow's alias
        new_name: The new flow's name
        realm: Target realm (uses default if not specified)

    Returns:
        Status message
    """
    copy_data = {"newName": new_name}

    await client._make_request(
        "POST", f"/authentication/flows/{flow_alias}/copy", data=copy_data, realm=realm
    )
    return {
        "status": f"Authentication flow '{flow_alias}' copied to '{new_name}' successfully"
    }


# Flow Executions Tools


@mcp.tool()
async def get_flow_executions(
    flow_alias: str,
    realm: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Get authentication executions for a flow.

    Args:
        flow_alias: The flow's alias
        realm: Target realm (uses default if not specified)

    Returns:
        List of execution objects
    """
    return await client._make_request(
        "GET", f"/authentication/flows/{flow_alias}/executions", realm=realm
    )


@mcp.tool()
async def update_flow_executions(
    flow_alias: str,
    executions: List[Dict[str, Any]],
    realm: Optional[str] = None,
) -> Dict[str, str]:
    """
    Update authentication executions of a flow.

    Args:
        flow_alias: The flow's alias
        executions: List of execution objects with updated properties
        realm: Target realm (uses default if not specified)

    Returns:
        Status message
    """
    await client._make_request(
        "PUT",
        f"/authentication/flows/{flow_alias}/executions",
        data=executions,
        realm=realm,
    )
    return {"status": f"Flow executions updated successfully"}


@mcp.tool()
async def add_execution_to_flow(
    flow_alias: str,
    provider: str,
    realm: Optional[str] = None,
) -> Dict[str, str]:
    """
    Add a new authentication execution to a flow.

    Args:
        flow_alias: The flow's alias
        provider: The authenticator provider
        realm: Target realm (uses default if not specified)

    Returns:
        Status message
    """
    execution_data = {"provider": provider}

    await client._make_request(
        "POST",
        f"/authentication/flows/{flow_alias}/executions/execution",
        data=execution_data,
        realm=realm,
    )
    return {"status": f"Execution '{provider}' added to flow successfully"}


@mcp.tool()
async def add_subflow_to_flow(
    flow_alias: str,
    alias: str,
    type: str = "basic-flow",
    id: Optional[str] = None,
    description: Optional[str] = None,
    provider: Optional[str] = None,
    realm: Optional[str] = None,
) -> Dict[str, str]:
    """
    Add a new flow with new execution to existing flow.

    Args:
        flow_alias: The parent flow's alias
        alias: The new subflow's alias
        type: Flow type (basic-flow, form-flow, etc.)
        id: Subflow ID
        description: Subflow description
        provider: Provider ID
        realm: Target realm (uses default if not specified)

    Returns:
        Status message
    """
    subflow_data = {"alias": alias, "type": type}

    if id is not None:
        subflow_data["id"] = id
    if description:
        subflow_data["description"] = description
    if provider:
        subflow_data["provider"] = provider

    await client._make_request(
        "POST",
        f"/authentication/flows/{flow_alias}/executions/flow",
        data=subflow_data,
        realm=realm,
    )
    return {"status": f"Subflow '{alias}' added to flow successfully"}


# Execution Management Tools


@mcp.tool()
async def get_execution(
    execution_id: str,
    realm: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Get a single authentication execution.

    Args:
        execution_id: The execution's ID
        realm: Target realm (uses default if not specified)

    Returns:
        Execution object
    """
    return await client._make_request(
        "GET", f"/authentication/executions/{execution_id}", realm=realm
    )


@mcp.tool()
async def delete_execution(
    execution_id: str,
    realm: Optional[str] = None,
) -> Dict[str, str]:
    """
    Delete an authentication execution.

    Args:
        execution_id: The execution's ID
        realm: Target realm (uses default if not specified)

    Returns:
        Status message
    """
    await client._make_request(
        "DELETE", f"/authentication/executions/{execution_id}", realm=realm
    )
    return {"status": "Execution deleted successfully"}


@mcp.tool()
async def raise_execution_priority(
    execution_id: str,
    realm: Optional[str] = None,
) -> Dict[str, str]:
    """
    Raise an execution's priority.

    Args:
        execution_id: The execution's ID
        realm: Target realm (uses default if not specified)

    Returns:
        Status message
    """
    await client._make_request(
        "POST", f"/authentication/executions/{execution_id}/raise-priority", realm=realm
    )
    return {"status": "Execution priority raised successfully"}


@mcp.tool()
async def lower_execution_priority(
    execution_id: str,
    realm: Optional[str] = None,
) -> Dict[str, str]:
    """
    Lower an execution's priority.

    Args:
        execution_id: The execution's ID
        realm: Target realm (uses default if not specified)

    Returns:
        Status message
    """
    await client._make_request(
        "POST", f"/authentication/executions/{execution_id}/lower-priority", realm=realm
    )
    return {"status": "Execution priority lowered successfully"}


@mcp.tool()
async def create_execution(
    id: Optional[str] = None,
    authenticator: Optional[str] = None,
    authenticator_flow: Optional[bool] = None,
    authenticator_config: Optional[str] = None,
    flow_id: Optional[str] = None,
    parent_flow: Optional[str] = None,
    priority: Optional[int] = None,
    requirement: Optional[str] = None,
    realm: Optional[str] = None,
) -> Dict[str, str]:
    """
    Add a new authentication execution.

    Args:
        id: Execution ID
        authenticator: Authenticator name
        authenticator_flow: Is this an authenticator flow
        authenticator_config: Authenticator configuration
        flow_id: Flow ID
        parent_flow: Parent flow ID
        priority: Priority level
        requirement: Requirement level (DISABLED, ALTERNATIVE, REQUIRED, CONDITIONAL)
        realm: Target realm (uses default if not specified)

    Returns:
        Status message
    """
    execution_data = {}

    if id is not None:
        execution_data["id"] = id
    if authenticator is not None:
        execution_data["authenticator"] = authenticator
    if authenticator_flow is not None:
        execution_data["authenticatorFlow"] = authenticator_flow
    if authenticator_config is not None:
        execution_data["authenticatorConfig"] = authenticator_config
    if flow_id is not None:
        execution_data["flowId"] = flow_id
    if parent_flow is not None:
        execution_data["parentFlow"] = parent_flow
    if priority is not None:
        execution_data["priority"] = priority
    if requirement is not None:
        execution_data["requirement"] = requirement

    await client._make_request(
        "POST", "/authentication/executions", data=execution_data, realm=realm
    )
    return {"status": "Execution created successfully"}


# Authenticator Configuration Tools


@mcp.tool()
async def get_authenticator_config(
    config_id: str,
    realm: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Get authenticator configuration.

    Args:
        config_id: The configuration's ID
        realm: Target realm (uses default if not specified)

    Returns:
        Configuration object
    """
    return await client._make_request(
        "GET", f"/authentication/config/{config_id}", realm=realm
    )


@mcp.tool()
async def create_authenticator_config(
    alias: str,
    config: Dict[str, Any],
    id: Optional[str] = None,
    realm: Optional[str] = None,
) -> Dict[str, str]:
    """
    Create new authenticator configuration.

    Args:
        alias: Configuration alias
        config: Configuration values
        id: Configuration ID
        realm: Target realm (uses default if not specified)

    Returns:
        Status message with configuration ID
    """
    config_data = {"alias": alias, "config": config}

    if id is not None:
        config_data["id"] = id

    response = await client._make_request(
        "POST", "/authentication/config", data=config_data, realm=realm
    )
    return {
        "status": "Configuration created successfully",
        "id": response.get("id", ""),
    }


@mcp.tool()
async def update_authenticator_config(
    config_id: str,
    alias: str,
    config: Dict[str, Any],
    id: Optional[str] = None,
    realm: Optional[str] = None,
) -> Dict[str, str]:
    """
    Update authenticator configuration.

    Args:
        config_id: The configuration's ID (used in URL path)
        alias: Configuration alias
        config: Configuration values
        id: Configuration ID (for request body)
        realm: Target realm (uses default if not specified)

    Returns:
        Status message
    """
    config_data = {"alias": alias, "config": config}

    if id is not None:
        config_data["id"] = id

    await client._make_request(
        "PUT", f"/authentication/config/{config_id}", data=config_data, realm=realm
    )
    return {"status": "Configuration updated successfully"}


@mcp.tool()
async def delete_authenticator_config(
    config_id: str,
    realm: Optional[str] = None,
) -> Dict[str, str]:
    """
    Delete authenticator configuration.

    Args:
        config_id: The configuration's ID
        realm: Target realm (uses default if not specified)

    Returns:
        Status message
    """
    await client._make_request(
        "DELETE", f"/authentication/config/{config_id}", realm=realm
    )
    return {"status": "Configuration deleted successfully"}


@mcp.tool()
async def get_execution_config(
    execution_id: str,
    config_id: str,
    realm: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Get execution's configuration.

    Args:
        execution_id: The execution's ID
        config_id: The configuration's ID
        realm: Target realm (uses default if not specified)

    Returns:
        Configuration object
    """
    return await client._make_request(
        "GET",
        f"/authentication/executions/{execution_id}/config/{config_id}",
        realm=realm,
    )


@mcp.tool()
async def update_execution_config(
    execution_id: str,
    authenticator_config: Dict[str, Any],
    id: Optional[str] = None,
    realm: Optional[str] = None,
) -> Dict[str, str]:
    """
    Update execution with new configuration.

    Args:
        execution_id: The execution's ID
        authenticator_config: New configuration data
        id: Configuration ID
        realm: Target realm (uses default if not specified)

    Returns:
        Status message
    """
    config_data = authenticator_config.copy()

    if id is not None:
        config_data["id"] = id

    await client._make_request(
        "POST",
        f"/authentication/executions/{execution_id}/config",
        data=config_data,
        realm=realm,
    )
    return {"status": "Execution configuration updated successfully"}


# Provider Tools


@mcp.tool()
async def get_authenticator_providers(
    realm: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Get authenticator providers.

    Args:
        realm: Target realm (uses default if not specified)

    Returns:
        List of authenticator provider objects
    """
    return await client._make_request(
        "GET", "/authentication/authenticator-providers", realm=realm
    )


@mcp.tool()
async def get_client_authenticator_providers(
    realm: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Get client authenticator providers.

    Args:
        realm: Target realm (uses default if not specified)

    Returns:
        List of client authenticator provider objects
    """
    return await client._make_request(
        "GET", "/authentication/client-authenticator-providers", realm=realm
    )


@mcp.tool()
async def get_provider_config_description(
    provider_id: str,
    realm: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Get authenticator provider's configuration description.

    Args:
        provider_id: The provider's ID
        realm: Target realm (uses default if not specified)

    Returns:
        Provider configuration description object
    """
    return await client._make_request(
        "GET", f"/authentication/config-description/{provider_id}", realm=realm
    )


# Required Actions Tools


@mcp.tool()
async def get_required_actions(
    realm: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Get all required actions in the realm.

    Args:
        realm: Target realm (uses default if not specified)

    Returns:
        List of required action objects
    """
    return await client._make_request(
        "GET", "/authentication/required-actions", realm=realm
    )


@mcp.tool()
async def get_required_action(
    alias: str,
    realm: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Get a specific required action by alias.

    Args:
        alias: The required action's alias
        realm: Target realm (uses default if not specified)

    Returns:
        Required action object
    """
    return await client._make_request(
        "GET", f"/authentication/required-actions/{alias}", realm=realm
    )


@mcp.tool()
async def update_required_action(
    alias: str,
    name: str,
    enabled: bool = True,
    default_action: bool = False,
    priority: Optional[int] = None,
    config: Optional[Dict[str, Any]] = None,
    realm: Optional[str] = None,
) -> Dict[str, str]:
    """
    Update a required action.

    Args:
        alias: The required action's alias
        name: Display name
        enabled: Whether the action is enabled
        default_action: Whether this is a default action
        priority: Action priority
        config: Additional configuration
        realm: Target realm (uses default if not specified)

    Returns:
        Status message
    """
    action_data = {
        "alias": alias,
        "name": name,
        "enabled": enabled,
        "defaultAction": default_action,
    }

    if priority is not None:
        action_data["priority"] = priority
    if config:
        action_data["config"] = config

    await client._make_request(
        "PUT",
        f"/authentication/required-actions/{alias}",
        data=action_data,
        realm=realm,
    )
    return {"status": f"Required action '{alias}' updated successfully"}


@mcp.tool()
async def register_required_action(
    provider_id: str,
    name: str,
    realm: Optional[str] = None,
) -> Dict[str, str]:
    """
    Register a new required action.

    Args:
        provider_id: The provider ID
        name: Action name
        realm: Target realm (uses default if not specified)

    Returns:
        Status message
    """
    action_data = {"providerId": provider_id, "name": name}

    await client._make_request(
        "POST",
        "/authentication/register-required-action",
        data=action_data,
        realm=realm,
    )
    return {"status": f"Required action '{name}' registered successfully"}


@mcp.tool()
async def get_unregistered_required_actions(
    realm: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Get unregistered required actions.

    Args:
        realm: Target realm (uses default if not specified)

    Returns:
        List of unregistered required action objects
    """
    return await client._make_request(
        "GET", "/authentication/unregistered-required-actions", realm=realm
    )


@mcp.tool()
async def raise_required_action_priority(
    alias: str,
    realm: Optional[str] = None,
) -> Dict[str, str]:
    """
    Raise the priority of a required action.

    Args:
        alias: The required action's alias
        realm: Target realm (uses default if not specified)

    Returns:
        Status message
    """
    await client._make_request(
        "POST", f"/authentication/required-actions/{alias}/raise-priority", realm=realm
    )
    return {"status": f"Required action '{alias}' priority raised successfully"}


@mcp.tool()
async def lower_required_action_priority(
    alias: str,
    realm: Optional[str] = None,
) -> Dict[str, str]:
    """
    Lower the priority of a required action.

    Args:
        alias: The required action's alias
        realm: Target realm (uses default if not specified)

    Returns:
        Status message
    """
    await client._make_request(
        "POST", f"/authentication/required-actions/{alias}/lower-priority", realm=realm
    )
    return {"status": f"Required action '{alias}' priority lowered successfully"}
