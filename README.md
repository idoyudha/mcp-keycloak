# Keycloak MCP Server 
[![Python Version](https://img.shields.io/badge/python-3.13%2B-blue)](https://www.python.org/downloads/)
[![MIT licensed](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE.txt)
[![smithery badge](https://smithery.ai/badge/@idoyudha/mcp-keycloak)](https://smithery.ai/server/@idoyudha/mcp-keycloak)
[![Trust Score](https://archestra.ai/mcp-catalog/api/badge/quality/idoyudha/mcp-keycloak)](https://archestra.ai/mcp-catalog/idoyudha__mcp-keycloak)

A Model Context Protocol (MCP) server that provides a natural language interface for managing Keycloak identity and access management through its REST API. This server enables AI agents to perform user management, client configuration, realm administration, and role-based access control operations seamlessly.

## Overview

The Keycloak MCP Server bridges the gap between AI applications and Keycloak's powerful identity management capabilities. Whether you're building an AI assistant that needs to manage users, configure clients, or handle complex authorization scenarios, this server provides the tools you need through simple, natural language commands.

## Features

### 🔐 Comprehensive User Management
Manage users lifecycle from creation to deletion, including password resets, session management, and user attribute updates.

### 🏢 Client Configuration
Create and configure OAuth2/OIDC clients, manage client secrets, and handle service accounts programmatically.

### 👥 Role-Based Access Control
Define and assign realm and client-specific roles, manage user permissions, and implement fine-grained access control.

### 🏛️ Realm Administration
Configure realm settings, manage default groups, handle event configurations, and control realm-wide policies.

### 🔐 Authentication Management
Comprehensive authentication flow management including creating, updating, and deleting flows, managing executions, and configuring authenticators.

### 🔄 Group Management
Organize users into groups, manage group hierarchies, and handle group-based permissions efficiently.

## Installation

### Installing via Smithery

To install mcp-keycloak for Claude Desktop automatically via [Smithery](https://smithery.ai/server/mcp-keycloak):

```bash
npx -y @smithery/cli install mcp-keycloak --client claude
```

### Quick Start

Install using pip:
```bash
pip install mcp-keycloak
```

### Development Installation

Clone the repository and install dependencies:
```bash
git clone https://github.com/idoyudha/mcp-keycloak.git
cd mcp-keycloak
pip install -e .
```

## Configuration

The server can be configured using environment variables or a `.env` file:

```bash
# Required configuration
SERVER_URL=https://your-keycloak-server.com
USERNAME=admin-username
PASSWORD=admin-password
REALM_NAME=your-realm

# Optional OAuth2 client configuration
CLIENT_ID=optional-client-id
CLIENT_SECRET=optional-client-secret
```

## Tools

The Keycloak MCP Server provides a comprehensive set of tools organized by functionality:

### User Management
Complete user lifecycle management including:
- `list_users` - List users with pagination and filtering
- `create_user` / `update_user` / `delete_user` - Full CRUD operations
- `reset_user_password` - Password management
- `get_user_sessions` / `logout_user` - Session control
- `count_users` - User statistics

### Client Management
OAuth2/OIDC client configuration:
- `list_clients` / `get_client` / `create_client` - Client operations
- `get_client_secret` / `regenerate_client_secret` - Secret management
- `get_client_service_account` - Service account access
- `update_client` / `delete_client` - Client modifications

### Role Management
Fine-grained permission control:
- `list_realm_roles` / `create_realm_role` - Realm role operations
- `list_client_roles` / `create_client_role` - Client-specific roles
- `assign_realm_role_to_user` / `remove_realm_role_from_user` - Role assignments
- `get_user_realm_roles` / `assign_client_role_to_user` - User role queries

### Group Management
Hierarchical user organization:
- `list_groups` / `create_group` / `update_group` - Group operations
- `get_group_members` / `add_user_to_group` - Membership management
- `get_user_groups` / `remove_user_from_group` - User group associations

### Realm Administration
System-wide configuration:
- `get_accessible_realms` - List of accessible realms
- `get_realm_info` / `update_realm_settings` - Realm configuration
- `get_realm_events_config` / `update_realm_events_config` - Event management
- `add_realm_default_group` / `remove_realm_default_group` - Default settings

### Authentication Management
Complete authentication flow control:
- `list_authentication_flows` / `get_authentication_flow` - Flow management
- `create_authentication_flow` / `update_authentication_flow` - Flow CRUD operations
- `delete_authentication_flow` / `copy_authentication_flow` - Flow modifications
- `get_flow_executions` / `update_flow_executions` - Execution management
- `create_execution` / `delete_execution` - Execution lifecycle
- `get_authenticator_config` / `create_authenticator_config` - Configuration management
- `get_required_actions` / `update_required_action` - Required actions control

## Usage

### Running the Server

Start the MCP server directly:
```bash
python -m src.main
```

### Integration Examples

#### Prerequisites

Before integrating the Keycloak MCP Server, ensure you have one of the following installed:

- **uvx** (recommended): Install via `pip install uvx` or `pipx install uvx`
- **uv**: Follow [installation instructions](https://docs.astral.sh/uv/getting-started/installation/)
- **npm/npx**: For Smithery installation (comes with [Node.js](https://nodejs.org/))

#### Option 1: Using Smithery CLI (Recommended)

The easiest way - automatically configures everything for Claude Desktop:

```bash
npx @smithery/cli install @idoyudha/mcp-keycloak --client claude
```

This command will prompt you for the required configuration values and set up the server automatically.

#### Option 2: Using uvx (Manual Setup)

No cloning required! Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "keycloak": {
      "command": "uvx",
      "args": ["mcp-keycloak"],
      "env": {
        "SERVER_URL": "https://your-keycloak.com",
        "USERNAME": "admin",
        "PASSWORD": "admin-password",
        "REALM_NAME": "your-realm"
      }
    }
  }
}
```

#### Option 3: Local Development Setup

For development or customization:

1. Clone the repository:
```bash
git clone https://github.com/idoyudha/mcp-keycloak.git
cd mcp-keycloak
```

2. Add to your `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "keycloak": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/mcp-keycloak",
        "run",
        "python",
        "-m",
        "src"
      ],
      "env": {
        "SERVER_URL": "https://your-keycloak.com",
        "USERNAME": "admin",
        "PASSWORD": "admin-password",
        "REALM_NAME": "your-realm"
      }
    }
  }
}
```

💡 **Quick Tips:**
- Replace `/path/to/mcp-keycloak` with the actual path where you cloned the repository
- Ensure your Keycloak server URL includes the protocol (`https://` or `http://`)
- The `REALM_NAME` should match an existing realm in your Keycloak instance

## Example Use Cases

### 🤖 AI-Powered Identity Management
Build AI assistants that can handle user onboarding, permission management, and access control through natural language commands.

### 🔄 Automated User Provisioning
Create workflows that automatically provision users, assign roles, and configure client applications based on business rules.

### 📊 Identity Analytics
Query and analyze user data, session information, and access patterns to gain insights into your identity infrastructure.

### 🚀 DevOps Integration
Integrate Keycloak management into your CI/CD pipelines, allowing automated configuration of identity services.

## Requirements

- Python 3.8 or higher
- Keycloak server (tested with Keycloak 18+)
- Admin access to Keycloak realm

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues, questions, or contributions, please visit the [GitHub repository](https://github.com/idoyudha/mcp-keycloak).
