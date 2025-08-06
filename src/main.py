import sys
from .common.server import mcp

# Import all tool modules to register them with the MCP server
from . import tools
from .tools import user_tools
from .tools import client_tools
from .tools import realm_tools
from .tools import role_tools
from .tools import group_tools

class KeycloakMCPServer:
    def __init__(self):
        print("Starting the Keycloak MCP Server", file=sys.stderr)
        # FastMCP registers tools automatically when imported

    def run(self):
        mcp.run()

def main():
    server = KeycloakMCPServer()
    server.run()

if __name__ == "__main__":
    main()