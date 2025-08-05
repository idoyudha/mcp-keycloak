import sys
from src.common.server import mcp

class KeycloakMCPServer:
    def __init__(self):
        print("Starting the Keycloak MCP Server", file=sys.stderr)

    def run(self):
        mcp.run()

def main():
    server = KeycloakMCPServer()
    server.run()

if __name__ == "__main__":
    main()