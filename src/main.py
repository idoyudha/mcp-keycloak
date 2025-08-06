import sys
from common.server import mcp

# Import all tool modules to register them with the MCP server
import tools.user_tools
import tools.client_tools
import tools.realm_tools
import tools.role_tools
import tools.group_tools

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