"""
Keycloak MCP Server

A Python MCP server for managing Keycloak identity and access management.
Supports both stdio and HTTP transports.
"""

import logging
import os
import sys

import uvicorn
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import Response

# Import all tool modules to register them with the MCP server
from . import tools  # noqa: F401
from .common.server import mcp
from .tools import (
    client_tools,  # noqa: F401
    group_tools,  # noqa: F401
    realm_tools,  # noqa: F401
    role_tools,  # noqa: F401
    user_tools,  # noqa: F401
)

# Configure logging
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stderr)],
)
logger = logging.getLogger(__name__)


class OriginValidationMiddleware(BaseHTTPMiddleware):
    """Middleware to validate Origin header to prevent DNS rebinding attacks"""

    def __init__(self, app, allowed_origins=None):
        super().__init__(app)
        # Default to localhost origins for security
        self.allowed_origins = allowed_origins or {
            "http://localhost:8000",
            "http://127.0.0.1:8000",
            "null",  # For file:// origins in development
        }

    async def dispatch(self, request, call_next):
        # Skip validation for preflight OPTIONS requests
        if request.method == "OPTIONS":
            return await call_next(request)

        origin = request.headers.get("origin")

        # If no Origin header, allow (some clients don't send it)
        if not origin:
            return await call_next(request)

        # Validate origin against allowed list
        if origin not in self.allowed_origins:
            logger.warning(f"Blocked request from unauthorized origin: {origin}")
            return Response(
                content="Forbidden: Invalid origin",
                status_code=403,
                headers={"Content-Type": "text/plain"},
            )

        return await call_next(request)


def main():
    transport_mode = os.getenv("TRANSPORT", "stdio")

    if transport_mode == "http":
        logger.info("Keycloak MCP Server starting in HTTP mode...")

        # Create Starlette app with streamable HTTP
        app = mcp.streamable_http_app()

        # Get configuration from environment
        port = int(os.environ.get("PORT", "8000"))

        # Add security middleware (ORDER MATTERS)
        # 1. Origin validation middleware (REQUIRED by MCP spec)
        allowed_origins = {
            f"http://localhost:{port}",
            f"http://127.0.0.1:{port}",
            "null",  # For file:// origins
        }
        app.add_middleware(OriginValidationMiddleware, allowed_origins=allowed_origins)

        # 2. CORS middleware for browser-based clients
        app.add_middleware(
            CORSMiddleware,
            allow_origins=[f"http://localhost:{port}", f"http://127.0.0.1:{port}"],
            allow_credentials=True,
            allow_methods=["GET", "POST", "OPTIONS"],
            allow_headers=["*"],
            expose_headers=["mcp-session-id", "mcp-protocol-version"],
            max_age=86400,
        )

        logger.info(f"Listening on http://127.0.0.1:{port}/mcp/")

        # Run with uvicorn
        uvicorn.run(app, host="127.0.0.1", port=port, log_level="info")

    else:
        # stdio mode (default)
        logger.info("Keycloak MCP Server starting in stdio mode...")

        # Run with stdio transport
        mcp.run()


if __name__ == "__main__":
    main()
