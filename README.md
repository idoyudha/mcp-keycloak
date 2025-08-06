# Keycloak MCP Server

This MCP (Model Context Protocol) server provides tools for interacting with Keycloak REST API.

## Configuration

Create a `.env` file in the root directory with the following variables:

```
SERVER_URL=https://your-keycloak-server.com
USERNAME=admin-username
PASSWORD=admin-password
REALM_NAME=your-realm
CLIENT_ID=optional-client-id
CLIENT_SECRET=optional-client-secret
```

## Available Tools

### User Management
- `list_users` - List users with pagination and filtering
- `get_user` - Get a specific user by ID
- `create_user` - Create a new user
- `update_user` - Update user information
- `delete_user` - Delete a user
- `reset_user_password` - Reset user password
- `get_user_sessions` - Get active sessions for a user
- `logout_user` - Logout user from all sessions

### Client Management
- `list_clients` - List clients in the realm
- `get_client` - Get client by database ID
- `get_client_by_clientid` - Get client by client ID
- `create_client` - Create a new client
- `update_client` - Update client configuration
- `delete_client` - Delete a client
- `get_client_secret` - Get client secret
- `regenerate_client_secret` - Regenerate client secret
- `get_client_service_account` - Get service account for client

### Realm Management
- `get_realm_info` - Get current realm information
- `update_realm_settings` - Update realm settings
- `get_realm_events_config` - Get events configuration
- `update_realm_events_config` - Update events configuration
- `get_realm_default_groups` - Get default groups
- `add_realm_default_group` - Add default group
- `remove_realm_default_group` - Remove default group

### Role Management
- `list_realm_roles` - List realm roles
- `get_realm_role` - Get specific realm role
- `create_realm_role` - Create realm role
- `update_realm_role` - Update realm role
- `delete_realm_role` - Delete realm role
- `list_client_roles` - List client roles
- `create_client_role` - Create client role
- `assign_realm_role_to_user` - Assign realm roles to user
- `remove_realm_role_from_user` - Remove realm roles from user
- `get_user_realm_roles` - Get user's realm roles
- `assign_client_role_to_user` - Assign client roles to user

### Group Management
- `list_groups` - List all groups
- `get_group` - Get specific group
- `create_group` - Create new group
- `update_group` - Update group
- `delete_group` - Delete group
- `get_group_members` - Get group members
- `add_user_to_group` - Add user to group
- `remove_user_from_group` - Remove user from group
- `get_user_groups` - Get user's groups

## Usage

Run the MCP server:

```bash
python -m src.main
```

The server will start and display all registered tools.