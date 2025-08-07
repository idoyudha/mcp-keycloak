# Keycloak MCP Server 
[![Integration](https://github.com/redis/mcp-redis/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/redis/lettuce/actions/workflows/integration.yml)
[![Python Version](https://img.shields.io/badge/python-3.13%2B-blue)](https://www.python.org/downloads/)
[![MIT licensed](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE.txt)

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

### 🔄 Group Management
Organize users into groups, manage group hierarchies, and handle group-based permissions efficiently.

## Installation

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
- `get_realm_info` / `update_realm_settings` - Realm configuration
- `get_realm_events_config` / `update_realm_events_config` - Event management
- `add_realm_default_group` / `remove_realm_default_group` - Default settings

## Usage

### Running the Server

Start the MCP server directly:
```bash
python -m src.main
```

### Integration Examples

#### Claude Desktop

1. Clone the server:
```bash
git clone https://github.com/idoyudha/mcp-keycloak.git
```

2. Configure in `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "keycloak": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/mcp-keycloak",
        "run",
        "src/main.py"
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

#### Using uvx

```json
{
  "mcpServers": {
    "keycloak": {
      "command": "uvx",
      "args": [
        "mcp-keycloak"
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