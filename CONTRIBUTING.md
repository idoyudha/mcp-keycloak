# Contributing to Keycloak MCP Server

Thank you for your interest in contributing to the Keycloak MCP Server! This document provides guidelines and information for contributors.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Testing](#testing)
- [Submitting Changes](#submitting-changes)
- [Code Style](#code-style)
- [Project Structure](#project-structure)
- [Adding New Tools](#adding-new-tools)
- [Documentation](#documentation)

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for all contributors. Please be kind, professional, and constructive in all interactions.

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- A Keycloak server for testing (can be local or remote)
- Basic understanding of:
  - Keycloak administration
  - REST APIs
  - Model Context Protocol (MCP)

### Development Setup

1. **Fork and clone the repository:**
   ```bash
   git clone https://github.com/yourusername/mcp-keycloak.git
   cd mcp-keycloak
   ```

2. **Set up the development environment:**
   ```bash
   # Install uv (modern Python package manager)
   pip install uv
   
   # Install dependencies using uv
   uv sync
   ```

3. **Configure environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your Keycloak server details
   ```

4. **Verify the setup:**
   ```bash
   # Run the server using the provided script
   ./scripts/run_server.sh
   
   # Or manually with uv
   uv run python -m src
   ```

## Local Development

### Quick Start for Development

Once you have the development environment set up, here's your typical development workflow:

1. **Start the development server:**
   ```bash
   ./scripts/run_server.sh
   ```
   This runs the MCP server locally using `uv run python -m src`.

2. **Make your changes** to the code

3. **Format and lint your code:**
   ```bash
   ./scripts/fix_lint.sh
   ```
   This runs `uv run ruff format .` to automatically fix formatting issues.

4. **Test your changes** by connecting an MCP client (like Claude Desktop) to your local server

### Development Environment

- **Package Management:** This project uses [uv](https://docs.astral.sh/uv/) for fast, reliable Python package management
- **Formatting:** [Ruff](https://ruff.rs/) for code formatting and linting
- **Testing:** pytest for unit tests
- **Type Checking:** mypy for static type checking

### IDE Setup

For the best development experience:

1. **VS Code:** Install the Python extension and configure it to use the project's virtual environment
2. **Configure formatting on save** to use ruff
3. **Enable type checking** with mypy
4. **Set up pytest** for running tests directly in your IDE

## Making Changes

### Before You Start

1. **Check existing issues:** Look for existing issues or discussions related to your intended changes
2. **Create an issue:** For significant changes, create an issue to discuss the approach first
3. **Create a branch:** Use a descriptive branch name
   ```bash
   git checkout -b feature/add-authentication-flows
   git checkout -b fix/user-creation-bug
   git checkout -b docs/update-readme
   ```

### Development Workflow

1. **Write code** following the project's coding standards
2. **Add tests** for new functionality
3. **Update documentation** as needed
4. **Run formatting and linting:**
   ```bash
   # Fix code formatting and linting issues
   ./scripts/fix_lint.sh
   ```
5. **Test thoroughly** with a real Keycloak instance:
   ```bash
   # Run the development server
   ./scripts/run_server.sh
   ```
6. **Commit changes** with clear, descriptive messages

## Testing

### Running Tests

```bash
# Run all tests with uv
uv run pytest

# Run with coverage
uv run pytest --cov=src

# Run specific test file
uv run pytest tests/test_user_management.py
```

### Manual Testing

1. **Set up a test Keycloak instance:**
   ```bash
   # Using Docker (recommended for testing)
   docker run -p 8080:8080 -e KEYCLOAK_ADMIN=admin -e KEYCLOAK_ADMIN_PASSWORD=admin quay.io/keycloak/keycloak:latest start-dev
   ```

2. **Test with Claude Desktop or other MCP clients**

3. **Verify all tools work as expected**

### Writing Tests

- Write unit tests for new tools and utilities
- Use pytest fixtures for common setup
- Mock external API calls when appropriate
- Test error conditions and edge cases

Example test structure:
```python
import pytest
from unittest.mock import AsyncMock, patch
from src.tools.user_management_tools import create_user

@pytest.mark.asyncio
async def test_create_user_success():
    with patch('src.tools.keycloak_client.KeycloakClient._make_request') as mock_request:
        mock_request.return_value = {"id": "test-user-id"}
        
        result = await create_user(
            username="testuser",
            email="test@example.com",
            first_name="Test",
            last_name="User"
        )
        
        assert result["status"] == "User created successfully"
        mock_request.assert_called_once()
```

## Submitting Changes

### Pull Request Process

1. **Ensure your branch is up to date:**
   ```bash
   git checkout main
   git pull upstream main
   git checkout your-feature-branch
   git rebase main
   ```

2. **Push your changes:**
   ```bash
   git push origin your-feature-branch
   ```

3. **Create a pull request:**
   - Use a clear, descriptive title
   - Provide a detailed description of changes
   - Reference any related issues
   - Include testing instructions

### Pull Request Template

```markdown
## Description
Brief description of the changes.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Refactoring
- [ ] Other (please describe)

## Testing
- [ ] Unit tests added/updated
- [ ] Manual testing completed
- [ ] All tests pass

## Checklist
- [ ] Code follows the project's style guidelines
- [ ] Self-review of code completed
- [ ] Documentation updated
- [ ] No breaking changes (or clearly documented)
```

## Code Style

### Python Style Guidelines

- Follow [PEP 8](https://pep8.org/) style guide
- Use [Black](https://black.readthedocs.io/) for code formatting
- Use [Ruff](https://ruff.rs/) for linting
- Maximum line length: 88 characters

### Development Scripts

The project includes helpful scripts in the `scripts/` directory:

```bash
# Fix code formatting and linting issues
./scripts/fix_lint.sh

# Run the development server
./scripts/run_server.sh
```

### Manual Formatting Commands

If you prefer to run formatting commands directly:

```bash
# Format code with ruff
uv run ruff format .

# Check and fix linting issues
uv run ruff check --fix .
```

### Code Quality

- Write clear, self-documenting code
- Use meaningful variable and function names
- Add type hints for function parameters and return values
- Include docstrings for all public functions

Example function:
```python
@mcp.tool()
async def create_user(
    username: str,
    email: str,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    realm: Optional[str] = None,
) -> Dict[str, str]:
    """
    Create a new user in the Keycloak realm.

    Args:
        username: The user's username
        email: The user's email address
        first_name: The user's first name
        last_name: The user's last name
        realm: Target realm (uses default if not specified)

    Returns:
        Status message with user creation result
    """
    # Implementation here
```

## Project Structure

```
mcp-keycloak/
├── src/
│   ├── __init__.py
│   ├── main.py              # MCP server entry point
│   ├── common/
│   │   └── server.py        # MCP server setup
│   └── tools/
│       ├── __init__.py
│       ├── keycloak_client.py       # Keycloak API client
│       ├── user_management_tools.py # User management tools
│       ├── client_management_tools.py
│       ├── role_management_tools.py
│       ├── group_management_tools.py
│       ├── realm_management_tools.py
│       └── authentication_management_tools.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Pytest configuration
│   └── test_*.py            # Test files
├── README.md
├── CONTRIBUTING.md
├── LICENSE
├── pyproject.toml           # Project configuration
└── .env.example             # Environment variables template
```

## Adding New Tools

### Creating a New Tool

1. **Define the tool function** in the appropriate module
2. **Use the `@mcp.tool()` decorator**
3. **Follow the naming convention:** `verb_noun` (e.g., `create_user`, `list_clients`)
4. **Add comprehensive docstrings**
5. **Handle errors appropriately**
6. **Add tests**

### Tool Guidelines

- **Single responsibility:** Each tool should do one thing well
- **Consistent parameters:** Use similar parameter names across tools
- **Error handling:** Provide clear error messages
- **Documentation:** Include usage examples in docstrings
- **Optional parameters:** Use sensible defaults

### Example Tool Implementation

```python
@mcp.tool()
async def get_user_sessions(
    user_id: str,
    realm: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Get active sessions for a specific user.

    Args:
        user_id: The user's ID
        realm: Target realm (uses default if not specified)

    Returns:
        List of user session objects

    Raises:
        KeycloakError: If the user is not found or sessions cannot be retrieved
    """
    try:
        return await client._make_request(
            "GET", 
            f"/users/{user_id}/sessions", 
            realm=realm
        )
    except Exception as e:
        raise KeycloakError(f"Failed to get user sessions: {str(e)}")
```

## Documentation

### Updating Documentation

- **README.md:** Update tool lists and examples
- **Docstrings:** Keep function documentation current
- **Type hints:** Ensure all functions have proper type annotations
- **Examples:** Provide practical usage examples

### Documentation Standards

- Use clear, concise language
- Provide working examples
- Keep documentation in sync with code changes
- Include error conditions and troubleshooting tips

## Getting Help

- **Issues:** Use GitHub issues for bug reports and feature requests
- **Discussions:** Use GitHub discussions for questions and general discussion
- **Email:** Contact maintainers for security issues

## Recognition

Contributors will be recognized in:
- GitHub contributors list
- Release notes (for significant contributions)
- README acknowledgments

Thank you for contributing to the Keycloak MCP Server! Your contributions help make identity management more accessible through AI.