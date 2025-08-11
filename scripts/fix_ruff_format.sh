#!/bin/bash

# Script to fix ruff formatting issues
# Run from the project root directory

echo "Fixing ruff formatting issues..."
uv run ruff format .

# Check if the format command was successful
if [ $? -eq 0 ]; then
    echo "✓ Ruff formatting completed successfully"
else
    echo "✗ Ruff formatting failed"
    exit 1
fi