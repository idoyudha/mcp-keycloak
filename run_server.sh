#!/bin/bash

# Run the Keycloak MCP server

echo "Starting Keycloak MCP Server..."

# Change to src directory to ensure proper imports
cd src

# Run with uv
uv run python main.py